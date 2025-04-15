# Ways to Call MongoDB Queries
- 1. Direct Queries
- 2. Aggregation Queries

# **1. Direct Queries = CRUD Operations:**

- **Create:**

  - `insertOne(document)`: Inserts a single document into a collection.
  - `insertMany(documents)`: Inserts multiple documents into a collection.

- **Read:**

  - `find(filter)`: Retrieves documents that match the specified filter.
  - `findOne(filter)`: Retrieves a single document that matches the filter.
  - `distinct(field, filter)`: Finds the distinct values for a specified field across a collection.

- **Update:**

  - `updateOne(filter, update, options)`: Updates a single document matching the filter.
  - `updateMany(filter, update, options)`: Updates multiple documents matching the filter.
  - `replaceOne(filter, replacement, options)`: Replaces a single document matching the filter with a new document.

- **Delete:**
  - `deleteOne(filter)`: Deletes a single document matching the filter.
  - `deleteMany(filter)`: Deletes multiple documents matching the filter.

**2. Query and Projection Operators:**

- **Comparison Operators:**

  - `$eq`: Matches values that are equal to a specified value.
  - `$gt`: Matches values that are greater than a specified value.
  - `$gte`: Matches values that are greater than or equal to a specified value.
  - `$lt`: Matches values that are less than a specified value.
  - `$lte`: Matches values that are less than or equal to a specified value.
  - `$ne`: Matches values that are not equal to a specified value.
  - `$in`: Matches any of the values specified in an array.
  - `$nin`: Matches none of the values specified in an array.

- **Logical Operators:**

  - `$and`: Joins query clauses with a logical AND.
  - `$or`: Joins query clauses with a logical OR.
  - `$not`: Inverts the effect of a query expression.
  - `$nor`: Joins query clauses with a logical NOR.

- **Element Operators:**

  - `$exists`: Matches documents that have the specified field.
  - `$type`: Selects documents if a field is of the specified type.

- **Evaluation Operators:**

  - `$expr`: Allows the use of aggregation expressions within the query language.
  - `$jsonSchema`: Validates documents against the given JSON Schema.
  - `$mod`: Performs a modulo operation on the value of a field and selects documents with a specified result.
  - `$regex`: Selects documents where values match a specified regular expression.
  - `$text`: Performs text search.
  - `$where`: Matches documents that satisfy a JavaScript expression.

- **Array Operators:**

  - `$all`: Matches arrays that contain all elements specified in the query.
  - `$elemMatch`: Selects documents if an element in the array field matches all the specified `$elemMatch` conditions.
  - `$size`: Selects documents if the array field is a specified size.

- **Projection Operators:**
  - `$`: Projects the first element in an array that matches the query condition.
  - `$elemMatch`: Projects the first element in an array that matches the specified `$elemMatch` condition.
  - `$meta`: Projects the metadata associated with a text search score.
  - `$slice`: Limits the number of elements projected from an array.

**3. Update Operators:**

- **Field Update Operators:**

  - `$set`: Sets the value of a field.
  - `$unset`: Removes the specified field from a document.
  - `$rename`: Renames a field.

- **Array Update Operators:**

  - `$push`: Adds an element to an array.
  - `$pop`: Removes the first or last element of an array.
  - `$pull`: Removes all array elements that match a specified condition.
  - `$addToSet`: Adds elements to an array only if they do not already exist.

- **Bitwise Update Operators:**
  - `$bit`: Performs bitwise AND, OR, and XOR operations.