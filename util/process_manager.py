##
# Various routines for running processes from Python and parsing the output.
#


## Import
import subprocess


##
# Executes a process, parses the output streams as lists of utf-8 coded lines,
#    and returns a dict containing the parsed output
def run_command(command, stdin=None):
  output = subprocess.run(
    command,
    stdin=stdin,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
  )
  return {
    'stdout': output.stdout.decode('utf-8').splitlines(),
    'stderr': output.stderr.decode('utf-8').splitlines()
  }


##
# Parses a given list of output lines using a given regex and returns the
#   matches in a list
def parse_output(lines, regex):
  matches = []
  for line in lines:
    match = regex.search(line)
    if match:
      matches.append(match.groupdict())
  return matches


##
# Parses a given list of output lines using a given regex expecting exactly one
#   match. Throws an AssertionError unless exactly one match is found.
def parse_single_output(lines, regex):
  matches = parse_output(lines, regex)
  assert len(matches) == 1, "Exactly 1 match expected in the output"
  return matches[0]
