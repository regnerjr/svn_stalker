#!/usr/bin/env python

import sys
import pysvn
import time



def split_messages(long_line):
    splits=[message.message[x:x+40] for x in range(0,len(message.message),40)]
    return splits


# messages = client.log(SVN_PATH, discover_changed_paths=True, limit=3)
# print ""
# for message in messages:
#     print "%s -- r%s -- %s" % (message.author, message.revision.number, time.ctime(message.date))
#     message_list = split_messages(message.message)
#     for line in message_list:
#         if len(line) == 40: #append ... for lines that are continued.
#             line += "..."
#         print line
#     print ""
#     for path in message.changed_paths:
#         print "%s %s" % (path.action, path.path)
#     print "----------------------------------------"
def trim_trailing_slash(svn_url):
    #if the svn_url ends in a / chop it off
    if svn_url[-1] == '/':
        svn_url=svn_url[0:-1]
    return svn_url

def get_root_info(client, url):
    head_revision=pysvn.Revision( pysvn.opt_revision_kind.head )
    info = client.info2(url, revision=head_revision)
    #repo_name = SVN_URL.split('/')[-1]
    #the first item returned is the root of the request, which should
    #be the branch, or path of interest. This is a tuple of (path,svn_info)
    return info[0][1]

def get_diffs(client, root_info, diffs_to_get):
    head_revision = root_info.rev.number
    diffs_of_interest = range(head_revision-(diffs_to_get-1), head_revision+1)
    print "getting last %d diffs, from %s" % (diffs_to_get, root_info.URL)

# cat file.diff | sed 's/^-/\x1b[41m-/;s/^+/\x1b[42m+/;s/^@/\x1b[34m@/;s/$/\x1b[0m/'
# will print a colored diff to the terminal

def main():
    if len(sys.argv) == 1:
        print "Must supply a url for the repo you would like to stalk"
        sys.exit

    SVN_URL=sys.argv[1]
    SVN_URL = trim_trailing_slash(SVN_URL)

    client = pysvn.Client()
    root_info = get_root_info(client, SVN_URL)

    #maybe read this from a config file later
    diffs_to_get = 5
    get_diffs(client, root_info, diffs_to_get)

if __name__ == "__main__":
    main()
