from armedia.scrapers.movies.topcinema_scraper import (
    get_search_results_link,
    get_episodes_list,
    get_all_episodes_server_link,
)

def test_get_search_results_link():
    search_term = "black mirror"
    result = get_search_results_link(search_term)
    print(result)
    assert len(result) >= 6
    
def test_get_episodes_list():
    anime_link = "https://web.topcinema.cam/series/%d9%85%d8%b3%d9%84%d8%b3%d9%84-black-mirror-%d8%a7%d9%84%d9%85%d9%88%d8%b3%d9%85-%d8%a7%d9%84%d8%a7%d9%88%d9%84-%d9%85%d8%aa%d8%b1%d8%ac%d9%85/"
    result = get_episodes_list(anime_link)
    print(result)
    assert len(result) >= 3
    
def test_get_all_episodes_server_link():
    episode_link = "https://web.topcinema.cam/%d9%85%d8%b3%d9%84%d8%b3%d9%84-black-mirror-%d8%a7%d9%84%d9%85%d9%88%d8%b3%d9%85-%d8%a7%d9%84%d8%a7%d9%88%d9%84-%d8%a7%d9%84%d8%ad%d9%84%d9%82%d8%a9-1-%d9%85%d8%aa%d8%b1%d8%ac%d9%85%d8%a9/"
    result = get_all_episodes_server_link(episode_link)
    print(result)
    assert len(result) >= 8
    
if __name__ == "__main__":
    pass
    # test_get_search_results_link()
    # test_get_episodes_list()
    # test_get_all_episodes_server_link()