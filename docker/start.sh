#!/bin/sh
set -eu

if [ $# -eq 0 ]; then
    echo "usage: $0 <build|run|exec>"
    exit 1
fi

case "$1" in
    "build" )
        # Dockerイメージをビルド
        docker build \
            -t deepmimic \
            --network host \
            .
        ;;
    "run" )
        # Dockerコンテナを起動
        docker run \
            --name deepmimic \
            --rm -it \
            -v $PWD/../:/home/user/DeepMimic \
            deepmimic
        ;;
    "exec" )
        # 既に起動しているDockerコンテナにログイン
        docker exec -it deepmimic /bin/bash
        ;;
    *)
        echo "invalid args"
        ;;
esac

