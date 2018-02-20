# save return value to variable
puts 'save return value to variable'
x = 1

# Bad :-(
if x <= 1
  response = true
else
  response = false
end
puts response

# Good :-)
puts false unless x <= 1
# or
puts true if x <= 1

# String comparison
puts 'String comparison'
header = 'HEAD'
head = 'HEAD'

# Bad :-(
if header == head
  puts true
end

# Good :-)
puts true if header.eql? head
# or
puts false unless header.eql? head


i = 1
i = i + 1
puts i

i = 1
i += 1
puts i

# Nested if else
puts 'def my_method'
def my_method
  i = 5
  if i > 0
    puts 'i greater 0'
  end
end
my_method

def my_method
  i = 5
  puts 'i greater 0' unless i <0
end
my_method

# Calculate errors
puts 'calculate errors'
i = 0
exit_code = 0
exist = true
response_code = 2
ii = 5

# Bad :-(
if exist == true
  while i < ii
    if response_code == 2
      exit_code = exit_code + 1
    end
    i = i + 1
  end
end
if exit_code < 0
  puts false
else
  puts true
end

# Good :-)
if exist.eql? true
  while i < ii
    exit_code += 1 unless response_code.eql? 0
    i += 1
  end
end
puts true unless exit_code > 0
# or
puts true if exit_code.eql? 0
# or
puts false unless exit_code.eql? 0
