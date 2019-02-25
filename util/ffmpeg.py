##
# Various routines for running ffmpeg from Python and parsing the output.
#


## Import
import re
import process_manager, file_manager


##
# Calculates the bitrate of a given video file
def bitrate_of(video_path, duration_in_seconds):
  return file_manager.size_of(video_path) * 8 / duration_in_seconds


## Average SSIM regex
average_ssim_regex = re.compile(
  r"\[Parsed_ssim_0 @ [\dabcdef]*\] SSIM Y:(?P<y>\d+\.?\d*) \((?P<y_dB>(?:\d+\.?\d*)|(?:inf))\) U:(?P<u>\d+\.?\d*) \((?P<u_dB>(?:\d+\.?\d*)|(?:inf))\) V:(?P<v>\d+\.?\d*) \((?P<v_dB>(?:\d+\.?\d*)|(?:inf))\) All:(?P<all>\d+\.?\d*) \((?P<all_dB>(?:\d+\.?\d*)|(?:inf))\)"
)


## Average PSNR regex
average_psnr_regex = re.compile(
  r"\[Parsed_psnr_1 @ [\dabcdef]*\] PSNR y:(?P<y>(?:\d+\.?\d*)|(?:inf)) u:(?P<u>(?:\d+\.?\d*)|(?:inf)) v:(?P<v>(?:\d+\.?\d*)|(?:inf)) average:(?P<avg>(?:\d+\.?\d*)|(?:inf)) min:(?P<min>(?:\d+\.?\d*)|(?:inf)) max:(?P<max>(?:\d+\.?\d*)|(?:inf))"
)


## Framewise PSNR regex
framewise_psnr_regex = re.compile(
  r"^n:(?P<n>\d+)\s+mse_avg:(?P<mse_avg>(?:\d+\.?\d*)|(?:inf))\s+mse_y:(?P<mse_y>(?:\d+\.?\d*)|(?:inf))\s+mse_u:(?P<mse_u>(?:\d+\.?\d*)|(?:inf))\s+mse_v:(?P<mse_v>(?:\d+\.?\d*)|(?:inf))\s+psnr_avg:(?P<psnr_avg>(?:\d+\.?\d*)|(?:inf))\s+psnr_y:(?P<psnr_y>(?:\d+\.?\d*)|(?:inf))\s+psnr_u:(?P<psnr_u>(?:\d+\.?\d*)|(?:inf))\s+psnr_v:(?P<psnr_v>(?:\d+\.?\d*)|(?:inf))$"
)


## Framewise SSIM regex
framewise_ssim_regex = re.compile(
  r"^n:(?P<n>\d+)\s+Y:(?P<y>\d+\.?\d*)\s+U:(?P<u>\d+\.?\d*)\s+V:(?P<v>\d+\.?\d*)\s+All:(?P<all>\d+\.?\d*)\s+\((?P<db>(?:\d+\.?\d*)|(?:inf))\)$"
)


##
# Extracts average PSNR and SSIM from a video
def quality_of(lossy_video_path, source_video_path):
  output = process_manager.run_command([
    "ffmpeg",
    "-i", lossy_video_path,
    "-i", source_video_path,
    "-lavfi", "ssim;=-[0:v][1:v]psnr=-",
    "-f", "null",
    "-"
  ])

  return {
    'avg_ssim': process_manager.parse_single_output(
      output['stderr'],
      average_ssim_regex
    ),
    'avg_psnr': process_manager.parse_single_output(
      output['stderr'],
      average_psnr_regex
    ),
    'frm_ssim': process_manager.parse_output(
      output['stdout'],
      framewise_ssim_regex
    ),
    'frm_psnr': process_manager.parse_output(
      output['stdout'],
      framewise_psnr_regex
    ),
  }