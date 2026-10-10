cd /home/user/Bernard/lab/longform/lustig
python3 -c "
import sys, os; sys.path.insert(0, '..'); import doc
doc.deliver('build/lustig_hq.mkv', 'out/lustig_1080p.mp4', 896.03)
" && echo DELIVER_OK
