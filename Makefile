.PHONY: ci
list_repos:
	curl -s https://api.github.com/orgs/openelections/repos\?per_page\=200 \
	  | jq '.[] | select(.name | contains("openelections-results")) | .git_url' | sort

.PHONY: python-format-all
python-format-all:
	git ls-files -- './*.py' | xargs yapf -i
