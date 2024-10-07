from django.db import models

from django.contrib.auth.models import User  # Optional: if you want to associate data with users

# Model to store the appliance usage details
class ApplianceUsage(models.Model):
    # Optional: ForeignKey to link usage data with a specific user
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    # Appliance details
    appliance_name = models.CharField(max_length=255)
    num_appliances = models.IntegerField()
    wattage = models.FloatField()
    time_on = models.FloatField()
    
    # Date and time when the entry was created
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.appliance_name} - {self.num_appliances} appliance(s)"

# Model to store the predicted budget for a user
class PredictedBudget(models.Model):
    # Optional: ForeignKey to link the prediction with a specific user
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    # Relationship to the appliance usage data
    appliance_usage = models.ManyToManyField(ApplianceUsage)

    # Predicted budget
    predicted_budget = models.FloatField()

    # Date and time when the prediction was made
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Predicted Budget: {self.predicted_budget}"
