from armedia.scrapers.anime.anime_sanka_scraper import (
    get_search_results_link,
    get_all_episodes_server_link,
)


def test_get_search_results_link():
    search_term = "fire force"
    result = get_search_results_link(search_term)
    print(result)
    assert len(result) >= 2


def test_get_all_episodes_server_link():
    anime_link = "https://ww.anime-sanka.com/2022/06/fire-force-1080p_6.html"
    result = get_all_episodes_server_link(anime_link)
    print(result)
    assert len(result) > 2


if __name__ == "__main__":
    pass
    # test_get_search_results_link()
    # test_get_all_episodes_server_link()
