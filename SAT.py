import copy

def pruner(claim,var,val):
  result = []
  for clause in claim:
    if var not in clause and "n"+var not in clause:
      result.append(clause)
      continue
    if var in clause:
      if val == 1:
        continue
      elif val == 0:
        while var in clause:
          idx = clause.index(var)
          del clause[idx]
        if(len(clause) == 0):
          result.append([-1])
        else:
          result.append(clause)
    if "n" + var in clause:
      if val == 0:
        continue
      if val == 1:
        while "n"+var in clause:
          idx = clause.index("n"+var)
          del clause[idx]
        if(len(clause)==0):
          result.append([-1])
        else:
          result.append(clause)
  return result

def variable_parser(claim):
  var_map = {}
  for clause in claim:
    for var in clause:
      if var[0]=='n':
         tok = var[1]
      else:
         tok = var[0]
      if tok not in var_map:
        var_map[tok] = 0
  return var_map

def DPLL(assignment,claim):
  var_map = variable_parser(claim)
  variables = list(var_map.keys())
  the_var = variables[0]
  if len(variables) == 1:
    for clause in claim:
      if clause != claim[0]:
        return False
    if claim[0][0][0] == "n":
       assignment[variables[0]] = 0
    else:
       assignment[variables[0]] = 1
    print(assignment) 
    return True
  else:
    assign1 = assignment.copy()
    assign1[the_var] = 0
    claim1 = pruner(copy.deepcopy(claim),the_var,0)
    assign2 = assignment.copy()
    assign2[the_var] = 1
    claim2 = pruner(copy.deepcopy(claim),the_var,1)
    #print("THE CLAIM",claim,"THE_VAR",the_var,"CLAIM1",claim1,"CLAIM2",claim2)
  if(len(claim1) == 0):
    print(assign1)
    return True
  elif(len(claim2) == 0):
    print(assign2)
    return True

  flag_1 = True
  flag_2 = True
  for c in claim1:
    if -1 in c:
      flag_1 = False
  for c in claim2:
    if -1 in c:
      flag_2 = False
  del var_map[the_var]
  return (flag_1 and DPLL(assign1,claim1)) or (flag_2 and DPLL(assign2,claim2))
  

def SAT_solver(claim):
  # parse first time to see what variables need to be included
  var_map = variable_parser(claim)
  variables = list(var_map.keys())
  if(len(variables) == 0):
    return True
  assignment_map = {}
  return DPLL(assignment_map,copy.deepcopy(claim))

# PROBLEM SET
claim1 = [["a","b","nc"],["a","nd"]]
claim2 = [["x","y","z"],["x","y","nz"],["x","ny","z"],["x","ny","nz"],["nx","y","z"],["nx","y","nz"],["nx","ny","z"],["nx","ny","nz"]]

# EXTRT TEST
claim3 = [["x","y"],["x","nu","w"],["nx","nu","w","z"]]
claim4 = [["x","y"],["y","nz","w"],["nx","ny"],["nx","nz","nw"],["x"]]

print(SAT_solver(claim1))
print(SAT_solver(claim2))

#print(SAT_solver(claim3))
#print(SAT_solver(claim4))
