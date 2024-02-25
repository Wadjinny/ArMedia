from armedia.scrapers.anime.witanime_scraper import (
    get_search_results_link,
    get_episodes_list,
    get_all_episodes_server_link,
)

def test_get_search_results_link():
    search_term = "naruto"
    result = get_search_results_link(search_term)
    print(result)
    assert len(result) > 5
    
def test_get_episodes_list():
    anime_link = "https://witanime.one/anime/boruto-naruto-next-generations/"
    result = get_episodes_list(anime_link)
    print(result)
    assert len(result) > 200
    
def test_get_all_episodes_server_link():
    episode_link = "https://witanime.one/episode/boruto-naruto-next-generations-%d8%a7%d9%84%d8%ad%d9%84%d9%82%d8%a9-278/"
    result = get_all_episodes_server_link(episode_link)
    print(result)
    assert len(result) > 4
    
if __name__ == "__main__":
    pass
    # test_get_search_results_link()
    # test_get_episodes_list()
    # test_get_all_episodes_server_link()