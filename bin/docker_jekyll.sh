docker run --rm \
  --volume="$PWD:/srv/jekyll:Z" \
  --publish [127.0.0.1]:4001:4001 \
  jekyll/jekyll \
  jekyll serve --livereload --config _config.yml,_config_dev.yml

