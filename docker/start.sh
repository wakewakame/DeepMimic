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
            . && \
        docker save deepmimic | xz -9 -c > deepmimic.tar.xz
        ;;
    "run" )
        # Dockerコンテナを起動
        docker run \
            --name deepmimic \
            --rm -it \
			-p 23389:3389 \
            -v $PWD/../:/home/user/DeepMimic \
            deepmimic \
			/bin/sh -c ' \
				echo user | sudo -S /etc/init.d/xrdp stop && \
				echo user | sudo -S /etc/init.d/xrdp start && \
				export DISPLAY=:10 && \
				/bin/bash \
			'
        ;;
    "exec" )
        # 既に起動しているDockerコンテナにログイン
        docker exec -it deepmimic /bin/bash
        ;;
    *)
        echo "invalid args"
        ;;
esac

