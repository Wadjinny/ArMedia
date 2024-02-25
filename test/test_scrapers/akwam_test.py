from armedia.scrapers.movies.akwam_scraper import (
    get_search_results_link,
    get_episodes_list,
    get_all_episodes_server_link,
)

def test_get_search_results_link():
    search_term = "black mirror"
    result = get_search_results_link(search_term)
    print(result)
    assert len(result) >= 5
    
def test_get_episodes_list():
    anime_link = "https://ak.sv/series/533/black-mirror-الموسم-الاول"
    result = get_episodes_list(anime_link)
    print(result)
    assert len(result) >= 3
    
def test_get_all_episodes_server_link():
    episode_link = "https://ak.sv/episode/8315/the-national-anthem"
    result = get_all_episodes_server_link(episode_link)
    print(result)
    assert len(result) >= 3
    
if __name__ == "__main__":
    pass
    # test_get_search_results_link()
    # test_get_episodes_list()
    test_get_all_episodes_server_link()