# Source Code

To generate artificial medical records using OpenAI GPT-3 API, execute the following from the root directory of the repository:

```bash
python code/generate_medical_records_from_openaigpt3.py
```

### Azure Functions
Code stored in code/TAforHealth_AzureFunc was used to deploy the Azure Function in the 2020Hack resource group (ta4h-func-app). This Azure function wraps the Text Analytics for Health endpoint, returning only the relevant HPO information. Note that the Text Analytics for Health endpoint is configurable from the Azure portal. It is currently set to the endpoint for the ta4h-app-service in the ta4health resource group. 
