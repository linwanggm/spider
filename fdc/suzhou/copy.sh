path=`pwd`"/data/"`date +%Y`
psql -c "copy suzhou_currentdata from '$path/current_time.txt' delimiter ','"
