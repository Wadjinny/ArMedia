from armedia.scrapers.anime.zimabadk_scraper import (
    get_search_results_link,
    get_episodes_list,
    get_all_episodes_server_link,
)

def test_get_search_results_link():
    search_term = "naruto"
    result = get_search_results_link(search_term)
    print(result)
    occurrences = sum(1 for item in result if search_term.lower() in item["name"].lower())
    assert occurrences >= 11, f'{occurrences=} {search_term=}'
    assert len(result) >= 11, f'{len(result)=} {search_term=}'
    
def test_get_episodes_list():
    anime_link = "https://www.zimabadk.com/anime/boruto-naruto-next-generations/"
    result = get_episodes_list(anime_link)
    print(result)
    assert len(result) > 200
    
def test_get_all_episodes_server_link():
    episode_link = "https://www.zimabadk.com/migi-to-dali-%d8%a7%d9%84%d8%ad%d9%84%d9%82%d8%a9-1/"
    result = get_all_episodes_server_link(episode_link)
    print(result)
    assert len(result) >= 6
    
if __name__ == "__main__":
    pass
    test_get_search_results_link()
    # test_get_episodes_list()
    # test_get_all_episodes_server_link()