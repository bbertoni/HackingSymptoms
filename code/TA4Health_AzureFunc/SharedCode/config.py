import os

# for local use only (uncomment below)
#text_analytics_endpoint = "<YOUR TEXT ANALYTICS FOR HEALTH APP SERVICE URL HERE>/text/analytics/v3.0-preview.1/domains/health"

# for deployed use (uncomment below)
text_analytics_endpoint = str(os.environ["text_analytics_endpoint"])