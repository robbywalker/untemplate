# Copyright 2010 The Untemplate Authors.  All Rights Reserved.

"""Reverse engineers templates."""


def getData(*docs):
  return None


def compareLists(a, b):
  """Computes the edit distance and list from the two lists.

  Uses the Levenshtein edit distance algorithm, with code modified from
  http://en.wikibooks.org/wiki/Algorithm_implementation/Strings/Levenshtein_distance#Python

  Returns:
    The edit distance, the edit list.
  """
  source_len, target_len = len(a), len(b)
  edit_lists = [[]]
  distance = [[]]
  for i in range(target_len+1):
    edit_lists[0].append(['I'] * i)
    distance[0].append(i)

  for j in range(1, source_len+1):
    edit_lists.append([['D'] * j])
    distance.append([j])

  for i in range(source_len):
    for j in range(target_len):
      cost = 1
      if a[i] == b[j]:
        cost = 0

      deletion = distance[i][j+1] + 1
      insertion = distance[i+1][j] + 1
      substitution = distance[i][j] + cost

      if deletion <= insertion and deletion <= substitution:
        # Deletion is best.
        best = deletion
        edit_list = list(edit_lists[i][j+1])
        edit_list.append('D')

      elif insertion <= substitution:
        # Insertion is best.
        best = insertion
        edit_list = list(edit_lists[i+1][j])
        edit_list.append('I')
        edit_lists[i+1].append(edit_list)

      else:
        # Substitution is best.
        best = substitution
        edit_list = list(edit_lists[i][j])
        if cost:
          edit_list.append('S')
        else:
          edit_list.append('=')

      edit_lists[i+1].append(edit_list)
      distance[i+1].append(best)

  return distance[source_len][target_len], edit_lists[source_len][target_len]
