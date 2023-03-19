from common.settings import SiteSettings
from site_API.utils.site_api_handler import SiteApiFactory

site = SiteSettings()

headers = {
    "X-RapidAPI-Key": site.api_key.get_secret_value(),
    "X-RapidAPI-Host": site.api_host
}

url = "https://" + site.api_host

params = {
    "players": {"page": "1", "per_page": "25"},
    "teams": {"page": "0"}
}

site_api = SiteApiFactory()

if __name__ == "__main__":
    site_api()
