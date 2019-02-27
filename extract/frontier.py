##
# Extracts the frontier rate-distortion curve for a given file
#


##
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..', 'util'))


## Import
from process_manager import run_command
from metric_manager  import quality_of, bitrate_of
from file_manager    import remove


def hevc_frontier(video_file, duration_in_seconds, params, tmp_file="tmp.mp4"):
  remove(tmp_file)
  results = []
  for param in params:
    run_command([
      "ffmpeg",
      "-i", video_file,
      "-c:v", "libx265",
    ] + param + [
      tmp_file
    ])
    quality = quality_of(video_file, tmp_file)
    bitrate = bitrate_of(tmp_file, duration_in_seconds)
    remove(tmp_file)
    results.append({
      'psnr': quality['avg_psnr'],
      'ssim': quality['avg_ssim'],
      'bitrate': bitrate,
    })
  return results




print(
  hevc_frontier(
    "",
    10,
    [[
      "-preset", "fast",
      "-t", "10",
      "-x265-params", ":".join([
        "bframes=0",
        "keyint=-1",
        "qp=%d" % qp
      ])
    ] for qp in [10, 20, 30, 40, 50]]
  )
)