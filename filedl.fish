#!/usr/bin/env fish
# download urls from a file with a pause in between while logging
set urlsfile $argv[1]

function logd -d 'dated log message'
    echo -e (date) "\t" $argv
end

if [ ! -f $urlsfile ]
    logd "ERROR: unable to find URLs file $urlsfile" 2>&1
    exit 1
end

mkdir -p IPEDS

for line in (cat $urlsfile)
    if string match -r -- '^\d{4}$' $line >/dev/null
        cd /Volumes/Arxiv/NCES
        set year $line
        logd "INFO: working on year $year"
        mkdir -p IPEDS/$year
        cd IPEDS/$year
    else
        set url $line
        logd "INFO: downloading $url"
        # probably should save HTTP status code because a lot come back 404
        curl --silent --show-error --remote-name --remote-header-name $url
        or logd "ERROR: failed to download $url" 2>&1
        sleep 1
    end
end
