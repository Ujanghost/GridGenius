import pandas as pd
import joblib
from django.shortcuts import render
from .models import ApplianceUsage, PredictedBudget
from sklearn.preprocessing import OneHotEncoder
from sklearn import __version__ as sklearn_version

# Load the trained model and encoder from the specified paths
model_filename = 'savedModels/random_forest_model.joblib'
encoder_filename = 'savedModels/onehot_encoder.joblib'
loaded_model = joblib.load(model_filename)
loaded_encoder = joblib.load(encoder_filename)

def prepare_user_features(appliance_usage):
    # Convert the appliance usage list to a DataFrame
    df = pd.DataFrame(appliance_usage)

    # Ensure that 'Appliance Name' is the only relevant feature for encoding
    if 'Appliance Name' not in df.columns:
        raise ValueError("'Appliance Name' column is missing in the input data")

    # Use the loaded encoder to transform the 'Appliance Name'
    appliance_name_encoded = loaded_encoder.transform(df[['Appliance Name']])
    
    # Convert to dense array if sparse
    if hasattr(appliance_name_encoded, 'toarray'):
        appliance_name_encoded = appliance_name_encoded.toarray()

    # Add the one-hot encoded features back to the DataFrame
    encoded_feature_names = loaded_encoder.get_feature_names_out(['Appliance Name'])
    appliance_name_df = pd.DataFrame(appliance_name_encoded, columns=encoded_feature_names)

    # Prepare the numerical features
    numerical_features = ['No of Appliances', 'Wattage', 'Time On (hours)']
    
    # Ensure all numerical features are present, fill with 0 if missing
    for feature in numerical_features:
        if feature not in df.columns:
            df[feature] = 0

    # Select only the required numerical features
    numerical_df = df[numerical_features]

    # Concatenate the numerical features with the one-hot encoded features
    final_df = pd.concat([numerical_df, appliance_name_df], axis=1)

    # Ensure the order of columns matches the training data
    expected_columns = numerical_features + encoded_feature_names.tolist()
    final_df = final_df.reindex(columns=expected_columns, fill_value=0)

    return final_df





# Main view for the application (renders the main.html form)
def predictor(request):
    return render(request, 'main.html')

# View function to handle the form submission and prediction
def formInfo(request):
    if request.method == 'POST':
        # Retrieve the data from the form
        appliance_names = request.POST.getlist('appliance_name[]')
        num_appliances_list = request.POST.getlist('num_appliances[]')
        wattage_list = request.POST.getlist('wattage[]')
        time_on_list = request.POST.getlist('time_on[]')

        # Prepare the appliance usage data
        appliance_usage = []
        appliance_usage_objects = []
        for i in range(len(appliance_names)):
            appliance = {
                "Appliance Name": appliance_names[i],
                "No of Appliances": int(num_appliances_list[i]),
                "Wattage": float(wattage_list[i]),
                "Time On (hours)": float(time_on_list[i])
            }
            appliance_usage.append(appliance)

            # Save each appliance usage to the database
            appliance_usage_obj = ApplianceUsage(
                appliance_name=appliance_names[i],
                num_appliances=int(num_appliances_list[i]),
                wattage=float(wattage_list[i]),
                time_on=float(time_on_list[i])
            )
            appliance_usage_obj.save()
            appliance_usage_objects.append(appliance_usage_obj)

        # Prepare the user features for the prediction
        user_features = prepare_user_features(appliance_usage)

        # Check if the user features are valid
        if user_features.isnull().values.any():
            return render(request, 'result.html', {'predicted_budget': 'Invalid input!'})

        # Make the prediction
        predicted_budget = loaded_model.predict(user_features)
        total_predicted_budget = sum(predicted_budget)

        # Save the predicted budget to the database
        predicted_budget_obj = PredictedBudget(
            predicted_budget=round(total_predicted_budget, 2)
        )
        predicted_budget_obj.save()

        # Associate the appliance usage with the predicted budget
        predicted_budget_obj.appliance_usage.set(appliance_usage_objects)
        predicted_budget_obj.save()

        # Render the result page with the prediction
        return render(request, 'result.html', {'predicted_budget': round(total_predicted_budget, 2)})

    # If it's not a POST request, render the main form page again
    return render(request, 'main.html')



