# Formatting
It is recommended to format the code before committing it. Here is some useful commands for code formatting (need yapf / isort / autoflake to be installed).
* _check_ means "only show change, not apply".
* _apply_ means "apply directly"

## yapf
bash path_to_project/check_format.sh
### check
yapf -p -r -d --style='{COLUMN_LIMIT:80}' ./
### apply
yapf -p -r -i --style='{COLUMN_LIMIT:80}' ./

## isort
Order is defined in _video_analyst/.isort.cfg_
### check
isort -rc -w 80 -d ./
### apply
isort -rc -w 80 ./

## flake
### check
autoflake -r ./
### apply
autoflake -r ./ -i
