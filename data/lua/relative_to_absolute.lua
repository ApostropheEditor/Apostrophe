function string.starts(String, Starts)
  any_start_with = false
  for i, Start in ipairs(Starts) do
    any_start_with = any_start_with or string.sub(String,1,string.len(Starts[i]))==Starts[i]
  end
  return any_start_with
end

function fix_path (path)
  if string.starts(path, {"/", "www.", "http", "file://", "#"}) then
    return path
  else
    return (pandoc.system.get_working_directory() or '') .. "/" .. path
  end
end

function Link (element)
  element.target = fix_path(element.target)
  return element
end

function Image (element)
  element.src = fix_path(element.src)
  return element
end
