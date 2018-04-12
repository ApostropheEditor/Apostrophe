function string.starts(String,Start)
   return string.sub(String,1,string.len(Start))==Start
end

function fix_path (path)
  if string.starts(path, "/") then
    return path
  else
    return (os.getenv('PANDOC_PREFIX') or '') .. path
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
