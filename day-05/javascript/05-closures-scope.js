function createIdGenerator(startAt = 1) {
  let nextId = startAt;

  return function generateId() {
    const currentId = nextId;
    nextId += 1;
    return currentId;
  };
}

const generateEmployeeId = createIdGenerator(1001);

console.log(generateEmployeeId());
console.log(generateEmployeeId());
console.log(generateEmployeeId());
