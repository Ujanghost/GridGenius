from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, MagicMock
from .models import ApplianceUsage, PredictedBudget
import pandas as pd

class PredictorViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('predictor')
        self.form_url = reverse('formInfo')
        self.appliance_data = {
            'appliance_name[]': ['Air Conditioner', 'Washing Machine'],
            'num_appliances[]': ['1', '2'],
            'wattage[]': ['2000', '500'],
            'time_on[]': ['5', '2']
        }

    def test_predictor_view_renders(self):
        """Test if predictor view renders the main form page."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')

    @patch('app.views.loaded_model')
    @patch('app.views.prepare_user_features')
    def test_formInfo_valid_post(self, mock_prepare_user_features, mock_loaded_model):
        """Test valid POST request to formInfo with proper model prediction."""
        # Mock the prepared features and model prediction
        mock_prepare_user_features.return_value = pd.DataFrame([[1, 2, 3, 4]], columns=['A', 'B', 'C', 'D'])
        mock_loaded_model.predict.return_value = [150.75]

        response = self.client.post(self.form_url, self.appliance_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'result.html')
        self.assertIn('predicted_budget', response.context)
        self.assertEqual(response.context['predicted_budget'], 150.75)

    @patch('app.views.loaded_model', None)
    def test_formInfo_model_not_loaded(self):
        """Test formInfo when model is not loaded."""
        response = self.client.post(self.form_url, self.appliance_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'result.html')
        self.assertIn('predicted_budget', response.context)
        self.assertEqual(response.context['predicted_budget'], 'Model not loaded!')

    def test_formInfo_input_length_mismatch(self):
        """Test input length mismatch handling in formInfo."""
        invalid_data = {
            'appliance_name[]': ['Air Conditioner'],
            'num_appliances[]': ['1', '2'],
            'wattage[]': ['2000'],
            'time_on[]': ['5']
        }
        response = self.client.post(self.form_url, invalid_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), "Input length mismatch")

    @patch('app.views.prepare_user_features', side_effect=ValueError('Encoder not loaded'))
    def test_formInfo_encoder_not_loaded(self, mock_prepare_user_features):
        """Test formInfo handling when encoder is not loaded or raises an error."""
        response = self.client.post(self.form_url, self.appliance_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'result.html')
        self.assertIn('predicted_budget', response.context)
        self.assertEqual(response.context['predicted_budget'], 'Error: Encoder not loaded')

    @patch('app.views.prepare_user_features', return_value=pd.DataFrame([[None]]))
    def test_formInfo_invalid_user_features(self, mock_prepare_user_features):
        """Test formInfo when prepared user features contain invalid values."""
        response = self.client.post(self.form_url, self.appliance_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'result.html')
        self.assertIn('predicted_budget', response.context)
        self.assertEqual(response.context['predicted_budget'], 'Invalid input!')
        
        
@patch('app.views.data_logging',return value=pd.Datafram
