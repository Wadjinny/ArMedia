from armedia.scrapers.movies.winnoise_scraper import (
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
    media_info = {'name': 'Black Season 1', 'id': '22859', 'type': 'TV'}
    result = get_episodes_list(media_desc=media_info)
    print(result)
    assert len(result) >= 18
    
def test_get_all_episodes_server_link():
    episode_info = {'id': '454387', 'number': "Eps 1: It's Not a Curse", 'type': 'TV'}
    result = get_all_episodes_server_link(episodes_desc=episode_info)
    print(result)
    assert len(result) >= 2
    
if __name__ == "__main__":
    pass
    # test_get_search_results_link()
    # test_get_episodes_list()
    # test_get_all_episodes_server_link()