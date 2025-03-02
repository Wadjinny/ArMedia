from armedia.scrapers.anime.animeiat_scraper import (
    get_search_results_link,
    get_episodes_list,
    get_all_episodes_server_link,
)

def test_get_search_results_link():
    search_term = "naruto"
    result = get_search_results_link(search_term)
    print(result)
    occurrences = sum(1 for item in result if search_term.lower() in item["name"].lower())
    assert occurrences >= 14, f'{occurrences=} {search_term=}'
    assert len(result) >= 14, f'{len(result)=} {search_term=}'
    
def test_get_episodes_list():
    anime_link = "https://www.animeiat.xyz/anime/enen-no-shouboutai"
    result = get_episodes_list(anime_link)
    print(result)
    assert len(result) ==24
    
    
def test_get_all_episodes_server_link():
    episode_link = "https://www.animeiat.xyz/watch/enen-no-shouboutai-episode-1"
    result = get_all_episodes_server_link(episode_link)
    print(result)
    assert len(result) >= 1
if __name__ == "__main__":
    pass
    test_get_search_results_link()
    # test_get_episodes_list()
    # test_get_all_episodes_server_link()