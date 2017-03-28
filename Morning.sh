# 环境初始化
killall vlc
/usr/bin/amixer set PCM 80%
/bin/su - pi -c '/usr/bin/nice -n -20 /usr/bin/nohup /usr/bin/cvlc --no-video --network-caching=1024 --audio-resampler 44100 --equalizer-preamp=10 --equalizer-bands="8 3 0 -2 -1 0.5 1.5 0.5 3 1.5" --compressor-attack=50 --compressor-release=500 --compressor-threshold=-20 --compressor-ratio=8 --compressor-knee=6 --compressor-makeup-gain=6 -L -I rc --rc-fake-tty --rc-host 127.0.0.1:8877 >/dev/null 2>&1 &'

# 启动电台
sleep 6s
echo volume 100 | /bin/nc -q 0 127.0.0.1 8877
echo add 'http://hls.qingting.fm:80/live/4576.m3u8?bitrate=64' | /bin/nc -q 0 127.0.0.1 8877

# 淡入电台
sleep 6s
/home/Morning/vlc/volume-alarm.sh

# 插播天气预报
sleep 2m
python /home/Morning/weather.py

# 播放60分钟后停止
sleep 60m
killall vlc