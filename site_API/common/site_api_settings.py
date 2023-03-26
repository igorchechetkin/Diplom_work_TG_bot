from common_settings.settings import SiteSettings


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
