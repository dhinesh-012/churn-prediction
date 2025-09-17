# src/preprocess_and_train.py
import os
import argparse
import pandas as pd
import joblib
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score

def get_data(db_url):
    engine = create_engine(db_url)
    df = pd.read_sql("SELECT * FROM customers;", engine)
    # normalize col names to lower
    df.columns = [c.lower() for c in df.columns]
    return df

def preprocess_and_train(db_url, save_path="models/churn_pipeline.joblib"):
    df = get_data(db_url)

    # basic cleaning
    # strip strings
    for c in df.select_dtypes(include=['object']).columns:
        df[c] = df[c].astype(str).str.strip()

    # Replace special "No internet service"/"No phone service"
    replace_no_internet = ['onlinesecurity','onlinebackup','deviceprotection','techsupport','streamingtv','streamingmovies']
    for col in replace_no_internet:
        if col in df.columns:
            df[col] = df[col].replace({'No internet service':'No'})

    if 'multiplelines' in df.columns:
        df['multiplelines'] = df['multiplelines'].replace({'No phone service':'No'})

    # drop or coerce types
    # ensure numeric columns exist
    numeric_cols = [c for c in ['tenure','monthlycharges','totalcharges','seniorcitizen'] if c in df.columns]
    # target
    df['churn'] = df['churn'].map({'Yes':1, 'No':0}).astype(int)

    X = df.drop(columns=['churn','customerid'] if 'customerid' in df.columns else ['churn'])
    y = df['churn']

    categorical_cols = [c for c in X.columns if c not in numeric_cols]

    # pipelines
    num_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    cat_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])
    preprocessor = ColumnTransformer([
        ('num', num_pipeline, numeric_cols),
        ('cat', cat_pipeline, categorical_cols)
    ])

    model = Pipeline([
        ('preproc', preprocessor),
        ('clf', RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1))
    ])

    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.20, random_state=42)

    print("Training ...")
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:,1]

    print("Classification report:\n", classification_report(y_test, y_pred))
    print("ROC AUC:", roc_auc_score(y_test, y_proba))

    # feature importance: need feature names after transformations
    # get numeric names + onehot names
    cat_ohe = model.named_steps['preproc'].named_transformers_['cat'].named_steps['onehot']
    cat_cols = categorical_cols
    try:
        cat_feature_names = list(cat_ohe.get_feature_names_out(cat_cols))
    except:
        # sklearn <1.0 fallback
        cat_feature_names = []
    feature_names = numeric_cols + cat_feature_names
    importances = model.named_steps['clf'].feature_importances_
    if len(feature_names) == len(importances):
        import pandas as pd
        feat_imp = pd.Series(importances, index=feature_names).sort_values(ascending=False)
        print("\nTop 15 feature importances:\n", feat_imp.head(15))
    else:
        print("Skipping feature importance (mismatch length).")

    os.makedirs(os.path.dirname(save_path) or '.', exist_ok=True)
    joblib.dump(model, save_path)
    print(f"Saved pipeline to {save_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", required=False, help="SQLAlchemy DB URL e.g. postgresql+psycopg2://user:pass@localhost:5432/churn_db. If not provided, uses env DATABASE_URL")
    parser.add_argument("--save", default="models/churn_pipeline.joblib")
    args = parser.parse_args()
    db_url = args.db or os.environ.get("DATABASE_URL") or "postgresql+psycopg2://churn_user:yourpassword@localhost:5432/churn_db"
    preprocess_and_train(db_url, args.save)
