.PHONY: ci
list_repos:	list_repos
	curl -s https://api.github.com/orgs/openelections/repos\?per_page\=200 \
	  | jq '.[] | select(.name | contains("openelections-data")) | .git_url' | sort
