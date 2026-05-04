import aiohttp
import asyncio

PLATFORMS = {
    "Instagram": {"url": "https://www.instagram.com/{}/", "icon": "https://www.google.com/s2/favicons?domain=instagram.com&sz=64"},
    "GitHub": {"url": "https://github.com/{}", "icon": "https://www.google.com/s2/favicons?domain=github.com&sz=64"},
    "X (Twitter)": {"url": "https://twitter.com/{}", "icon": "https://www.google.com/s2/favicons?domain=twitter.com&sz=64"},
    "Reddit": {"url": "https://www.reddit.com/user/{}", "icon": "https://www.google.com/s2/favicons?domain=reddit.com&sz=64"},
    "Pinterest": {"url": "https://www.pinterest.com/{}/", "icon": "https://www.google.com/s2/favicons?domain=pinterest.com&sz=64"},
    "TikTok": {"url": "https://www.tiktok.com/@{}", "icon": "https://www.google.com/s2/favicons?domain=tiktok.com&sz=64"},
    "Medium": {"url": "https://medium.com/@{}", "icon": "https://www.google.com/s2/favicons?domain=medium.com&sz=64"},
    "Vimeo": {"url": "https://vimeo.com/{}", "icon": "https://www.google.com/s2/favicons?domain=vimeo.com&sz=64"},
    "SoundCloud": {"url": "https://soundcloud.com/{}", "icon": "https://www.google.com/s2/favicons?domain=soundcloud.com&sz=64"},
    "Behance": {"url": "https://www.behance.net/{}", "icon": "https://www.google.com/s2/favicons?domain=behance.net&sz=64"},
    "Dribbble": {"url": "https://dribbble.com/{}", "icon": "https://www.google.com/s2/favicons?domain=dribbble.com&sz=64"},
    "Spotify": {"url": "https://open.spotify.com/user/{}", "icon": "https://www.google.com/s2/favicons?domain=spotify.com&sz=64"},
    "Steam": {"url": "https://steamcommunity.com/id/{}", "icon": "https://www.google.com/s2/favicons?domain=steamcommunity.com&sz=64"},
    "Twitch": {"url": "https://www.twitch.tv/{}", "icon": "https://www.google.com/s2/favicons?domain=twitch.tv&sz=64"},
    "LinkedIn": {"url": "https://www.linkedin.com/in/{}", "icon": "https://www.google.com/s2/favicons?domain=linkedin.com&sz=64"},
    "Tumblr": {"url": "https://{}.tumblr.com/", "icon": "https://www.google.com/s2/favicons?domain=tumblr.com&sz=64"},
    "Flickr": {"url": "https://www.flickr.com/people/{}/", "icon": "https://www.google.com/s2/favicons?domain=flickr.com&sz=64"},
    "Disqus": {"url": "https://disqus.com/by/{}/", "icon": "https://www.google.com/s2/favicons?domain=disqus.com&sz=64"},
    "Letterboxd": {"url": "https://letterboxd.com/{}/", "icon": "https://www.google.com/s2/favicons?domain=letterboxd.com&sz=64"},
    "Last.fm": {"url": "https://www.last.fm/user/{}", "icon": "https://www.google.com/s2/favicons?domain=last.fm&sz=64"},
    "Codecademy": {"url": "https://www.codecademy.com/profiles/{}", "icon": "https://www.google.com/s2/favicons?domain=codecademy.com&sz=64"},
    "DeviantArt": {"url": "https://www.deviantart.com/{}", "icon": "https://www.google.com/s2/favicons?domain=deviantart.com&sz=64"},
    "Patreon": {"url": "https://www.patreon.com/{}", "icon": "https://www.google.com/s2/favicons?domain=patreon.com&sz=64"},
    "Venmo": {"url": "https://venmo.com/{}", "icon": "https://www.google.com/s2/favicons?domain=venmo.com&sz=64"},
    "Bandcamp": {"url": "https://bandcamp.com/{}", "icon": "https://www.google.com/s2/favicons?domain=bandcamp.com&sz=64"}
}

async def check_platform(session, platform_name, url, icon_url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        async with session.get(url, headers=headers, timeout=5, allow_redirects=False) as response:
            if response.status == 200:
                content = await response.text()
                content_lower = content.lower()

                not_found_keywords = [
                    "page not found", "404", "not found", "doesn't exist", 
                    "user not found", "couldn't find that page", "sign up to see",
                    "login to continue", "the specified profile could not be found",
                    "this page could not be found", "profile not found",
                    "unavailable", "no user with that username"
                ]

                if any(keyword in content_lower for keyword in not_found_keywords):
                    return {"platform": platform_name, "url": url, "status": "Not Found", "icon": icon_url}

                return {"platform": platform_name, "url": url, "status": "Found", "icon": icon_url}
            else:
                return {"platform": platform_name, "url": url, "status": "Not Found", "icon": icon_url}
    except Exception as e:
         return {"platform": platform_name, "url": url, "status": "Error", "icon": icon_url}

async def search_profiles(username_data: dict):
    username = username_data["username"]
    score = username_data["score"]

    if not username:
        return

    async with aiohttp.ClientSession() as session:
        tasks = []
        for platform, info in PLATFORMS.items():
            url = info["url"].format(username)
            tasks.append(check_platform(session, platform, url, info["icon"]))

        for coro in asyncio.as_completed(tasks):
            result = await coro
            result["match_score"] = score
            yield result

def generate_usernames(first_name: str, last_name: str, dob: str = None):
    first = first_name.lower().strip()
    last = last_name.lower().strip()

    patterns = [
        (f"{first}{last}", 90),
        (f"{first}.{last}", 85),
        (f"{first}_{last}", 80),
        (f"{first}-{last}", 75),
        (f"{last}{first}", 70),
        (f"{first[0]}{last}", 65),
        (f"{first}{last[0]}", 60),
        (f"{first}{last}123", 40),
        (f"{first}{last}88", 35),
        (f"{first}{last}99", 35),
    ]

    if dob:
        year = dob.split('-')[0] if '-' in dob else ""
        day = dob.split('-')[2] if len(dob.split('-')) > 2 else ""
        month = dob.split('-')[1] if len(dob.split('-')) > 1 else ""

        if year:
            patterns.extend([
                (f"{first}{last}{year}", 99), 
                (f"{first}{year}", 50),
                (f"{last}{year}", 45),
                (f"{first}{last}{year[-2:]}", 95)
            ])
        if day and month:
             patterns.extend([
                 (f"{first}{last}{day}{month}", 80),
                 (f"{first}{day}{month}", 40)
             ])

    unique_usernames = {}
    for un, score in patterns:
        if un not in unique_usernames or score > unique_usernames[un]:
            unique_usernames[un] = score

    return [{"username": un, "score": s} for un, s in unique_usernames.items()]
