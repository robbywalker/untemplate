# Copyright 2010 The Untemplate Authors.  All Rights Reserved.

"""Reverse engineers templates."""


def getData(*docs):
  """ Takes docs and returns relevant data for each docs """
  # split docs into list of words
  split_docs = []
  split_docs = map(lambda(doc): doc.split(), docs)

  # make template
  template = makeTemplate(split_docs)
  #return template # uncomment to just get template for debugging

  # return list of lists of data
  data = map(lambda(doc): getDataFromDoc(doc, template), split_docs)
  return data



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


def makeTemplateFromPair(doc1, doc2):
  """ 
  Returns a list template given a pair of documents
  Notice that a template of the form returned by this 
  function can also be in input for generalization
  """
  # use the longest one as the source for consistency
  if len(doc1) >= len(doc2):
    longer = doc1
    shorter = doc2
  else: 
    longer = doc2
    shorter = doc1
  score, edit_list = compareLists(longer, shorter)

  # convert edit_list to template representation
  template = []
  for i in range(len(longer)):
    if edit_list[i] == '=':
      template.append(longer[i])
    else:
      template.append('*')

  return template

def makeTemplate(docs):
  """ 
  Makes the most general template given a collection of documents
  @ param docs - a list of documents
  """
  # handle trivial cases
  if len(docs) == 0:
    return None
  if len(docs) == 1:
    return docs[0]

  # apply pairwise templating
  template = makeTemplateFromPair(docs[0], docs[1])
  for i in range(1, len(docs)):
    template = makeTemplateFromPair(template, docs[i])

  return formatTemplate(template)

def formatTemplate(raw_template):
  """
  Get the template into the format we want for parsing.
  Interfaces with getDataFromDoc().
  Could replace with regex type thing eventually.
  """
  clean_template = []
  # Compress any runs of multiple *s into single *
  last = raw_template[0]
  clean_template.append(last)
  for i in range(1, len(raw_template)):
    if last == '*' and raw_template[i] == '*':
      continue
    else:
      last = raw_template[i]
      clean_template.append(last)
  return clean_template      

def getDataFromDoc(doc, template):
  """ 
  Applies template to doc to pull out content.
  Must interface with formatTemplate().
  Could eventually replace this with some regex thing.
  Use compareLists and state machine type implementation.
  """ 
  states = {'no_content' : 0, 'writing_content' : 1}
  state = states['no_content']
  matches = []
  # get edit_list which should only have '=' and runs of 'S'('I')* or 'D's
  score, edit_list = compareLists(template, doc)
  #print 'template: ', template 
  #print 'edit_list: ', edit_list
  #print 'doc: ', doc
  assert(len(edit_list) >= len(doc))

  current_matches = [] 
  # loop over edit_list to to find matches
  for i in range(len(edit_list)):
    if state == states['no_content']:
      # check whether to enter writing state
      if edit_list[i] == '=':
        continue
      elif edit_list[i] == 'D':
        matches.append([]) # signify empty frame
      elif edit_list[i] == 'S':
        state = states['writing_content']
        current_matches = [doc[i]]
    else: #state == states['writing_content']
      # check whether to stop writing content
      if edit_list[i] == '=':
        state = states['no_content']
        matches.append(current_matches)
        current_matches = [] 
      else:
        current_matches.append(doc[i])

  # add anything that was in writing state when loop ended 
  if len(current_matches) > 0:
    matches.append(current_matches)

  return matches 

