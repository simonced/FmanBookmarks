from fman import DirectoryPaneCommand, QuicksearchItem, show_quicksearch, \
    show_alert, show_prompt, show_status_message, \
    load_json, save_json
from fman.url import as_human_readable
import fman.fs as fs


#                      _              _
#                     | |            | |
#   ___ ___  _ __  ___| |_ __ _ _ __ | |_ ___
#  / __/ _ \| '_ \/ __| __/ _` | '_ \| __/ __|
# | (_| (_) | | | \__ \ || (_| | | | | |_\__ \
#  \___\___/|_| |_|___/\__\__,_|_| |_|\__|___/

BOOKMARKS_FILENAME = "Bookmarks.json"


#  _      _     _
# | |    (_)   | |
# | |     _ ___| |_
# | |    | / __| __|
# | |____| \__ \ |_
# |______|_|___/\__|

class BookmarksList(DirectoryPaneCommand):

    def __call__(self):
        # preload the bookmarks
        self.bookmarks = load_json(BOOKMARKS_FILENAME)

        result = show_quicksearch(self._listing)

        if result:
            query, value = result
            # show_alert('You typed %r and selected %r.' % (query, value))
            bookmark_path = self._findInBookmarks(value) # extract path of selected bookmark
            if bookmark_path and bookmark_path[0] and fs.exists(bookmark_path[0]['url']):
                self.pane.set_path(bookmark_path[0]['url'])


    # return list of available bookmarks
    def _listing(self, query):
        for item in self.bookmarks:
            try:
                index = item["name"].lower().index(query)
            except ValueError as not_found:
                continue
            else:
                # The characters that should be highlighted:
                highlight = range(index, index + len(query))
                yield QuicksearchItem(item["name"], \
                    description=as_human_readable(item["url"]), \
                    highlight=highlight)


    # filter available bookmarks to find the selection of the user
    def _findInBookmarks(self, value):
        return [x for x in self.bookmarks if x['name']==value]


#              _     _
#     /\      | |   | |
#    /  \   __| | __| |
#   / /\ \ / _` |/ _` |
#  / ____ \ (_| | (_| |
# /_/    \_\__,_|\__,_|

# Different command to add a new bookmark
class BookmarkAdd(DirectoryPaneCommand):
    def __call__(self):
        bookmarks = load_json(BOOKMARKS_FILENAME, default=[])
        current_folder = self.pane.get_path()
        # TODO check if it's already bookmarked and refuse to add a new entry

        bookmark_name, ok = show_prompt("Bookmark name:")
        if ok and bookmark_name:
            # new bookmark entry
            newBookmark = {}
            newBookmark["name"] = bookmark_name
            newBookmark["url"]  = current_folder
            # add new entry to list
            bookmarks.append(newBookmark)
            # save in json bookmarks file
            save_json(BOOKMARKS_FILENAME, bookmarks)
            show_status_message("Bookmark created.", 2)
        else:
            show_status_message("Bookmark not created.", 2)