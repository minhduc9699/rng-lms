def map_keys(l, key_field):
  return {
    str(obj[key_field]): obj
    for obj in l
  }