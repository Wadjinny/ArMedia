from armedia.scrapers.anime.zimabadk_scraper import (
    get_search_results_link,
    get_episodes_list,
    get_all_episodes_server_link,
)

def test_get_search_results_link():
    search_term = "naruto"
    result = get_search_results_link(search_term)
    print(result)
    assert len(result) >= 3
    
def test_get_episodes_list():
    anime_link = "https://www.zimabadk.com/anime/boruto-naruto-next-generations/"
    result = get_episodes_list(anime_link)
    print(result)
    assert len(result) > 200
    
def test_get_all_episodes_server_link():
    episode_link = "https://www.zimabadk.com/boruto-naruto-next-generations-e-279/"
    result = get_all_episodes_server_link(episode_link)
    print(result)
    assert len(result) >= 6
    
if __name__ == "__main__":
    pass
    # test_get_search_results_link()
    # test_get_episodes_list()
    # test_get_all_episodes_server_link()