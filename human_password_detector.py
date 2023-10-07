import pandas as pd
import numpy as np
import lightgbm as lgb

import argparse

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import roc_curve

from password_features import extract_features

def main(args):
    data = pd.read_csv(args.dataset)

    X = data.drop('human_created', axis=1)
    y = data['human_created']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a LightGBM model
    params = {
        'boosting_type': 'gbdt',
        'objective': 'binary',
        'metric': 'binary_logloss',
        'num_leaves': 31,
        'learning_rate': 0.05,
        'feature_fraction': 0.9
    }

    train_data = lgb.Dataset(X_train, label=y_train)
    gbm = lgb.train(params, train_data, num_boost_round=100)

    gbm.save_model('human_passwords_model.txt')

    # Make predictions
    y_pred = gbm.predict(X_test, num_iteration=gbm.best_iteration)
    y_pred_binary = [1 if prob > 0.5 else 0 for prob in y_pred]

    # Compute ROC curve
    fpr, tpr, thresholds = roc_curve(y_test, y_pred)

    # Get threshold for which the difference between TPR and FPR is maximum
    optimal_idx = np.argmax(tpr - fpr)
    optimal_threshold = thresholds[optimal_idx]

    print('Optimal Threshold:', optimal_threshold)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred_binary)
    print(f"Accuracy: {accuracy * 100:.2f}%")
    print(classification_report(y_test, y_pred_binary))

    optimal_threshold = 0.9 
    # Predict if a password is human-created
    new_password_features = extract_features(args.text)
    prediction = gbm.predict(pd.DataFrame([new_password_features]))
    is_human = prediction[0] > optimal_threshold
    print("Human created: ", is_human, optimal_threshold)

    ok = 0
    fail = 0
    load = False
    if load:
        with open(
            "english.txt", 'r', encoding='latin-1') as file:
            for line in file:
                password = line.strip()
                new_password_features = extract_features(password)
                prediction = gbm.predict(pd.DataFrame([new_password_features]))
                is_human = prediction[0] > optimal_threshold
                if is_human:
                    ok += 1
                else:
                    fail += 1
                print(password, is_human, prediction)

    gen = False
    if gen:
        for _ in range(1000):
            import random, string
            password = ''.join(random.choice(string.ascii_lowercase) for _ in range(random.randint(5, 16)))
            new_password_features = extract_features(password)
            prediction = gbm.predict(pd.DataFrame([new_password_features]))
            is_human = prediction[0] > optimal_threshold
            if is_human:
                ok += 1
            else:
                fail += 1
            print(password, is_human, prediction)

    print("Human: ", ok)
    print("Machine: ", fail)

    import matplotlib.pyplot as plt
    import seaborn as sns

    # Get feature importances
    feature_importances = gbm.feature_importance()

    # Get feature names
    feature_names = gbm.feature_name()

    # Create a DataFrame for feature importances
    feature_importance_df = pd.DataFrame({
        'Feature Name': feature_names,
        'Importance': feature_importances
    })

    # Sort the DataFrame by importance
    feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)

    # Print the feature importances
    print(feature_importance_df)

    # Set the width and height of the figure
    plt.figure(figsize=(10, 6))

    # Add title
    plt.title("Feature Importance")

    # Bar chart showing feature importance
    sns.barplot(x=feature_importance_df['Importance'], y=feature_importance_df['Feature Name'])

    # Add labels to your chart
    plt.xlabel('Feature Importance')
    plt.ylabel('Feature Names')

    plt.savefig('feature_importance_plot.png', bbox_inches='tight')

    # Show plot
    plt.show()
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Train LightGBM model and predict if text is likely a human-created password.')
    parser.add_argument('--dataset', type=str, required=True, help='Path to the input CSV dataset')
    parser.add_argument('--text', type=str, required=True, help='Text to predict as human-created password or not')
    args = parser.parse_args()
    main(args)
