## 🔹 Topic 1: `$match`

### 1. Conceptual Questions
- What is the purpose of `$match` in an aggregation pipeline?
- At what stage in the pipeline should `$match` be used for optimal performance?
- How does `$match` differ from `.find()` in terms of execution plan?

### 2. Hands-on with mflix (use `movies` collection)

✅ **Q1:** Fetch all movies released after 2010 that have a runtime greater than 120 minutes.
```js
db.movies.aggregate([
  { $match: { year: { $gt: 2010 }, runtime: { $gt: 120 } } }
])
```

✅ **Q2:** Find all documentaries (`genres`) with an IMDb rating greater than 7.5.

✅ **Q3:** Filter movies whose title contains the word `"Love"` and have a non-empty cast list.

✅ **Q4:** From `comments` collection, find all comments made by a specific user (e.g., `"blake@example.com"`) in 2015.

---

### 3. FAANG-Level Scenarios
- Why is `$match` placed at the beginning of a pipeline?
- What happens if `$match` is placed **after** `$project` or `$unwind`? When might that be useful?
- How does `$match` interact with indexes? Can it leverage covered indexes?
- What’s the performance impact of putting `$match` *after* `$lookup`?

---

## 🔹 Topic 2: `$project`

### 1. Conceptual Questions
- What is the role of `$project` in an aggregation pipeline?
- How can `$project` help in shaping documents before or after transformation?
- How do you rename fields or create computed fields using `$project`?
- Can you exclude `_id` in `$project`?

---

### 2. Hands-on with mflix (use `movies` collection)

✅ **Q1:** Display only `title`, `year`, and `genres` for all movies, excluding `_id`.
```js
db.movies.aggregate([
  {
    $project: {
      _id: 0,
      title: 1,
      year: 1,
      genres: 1
    }
  }
])
```

✅ **Q2:** Show `title`, and a new field `releaseDecade` = floor(year / 10) * 10.
(*Hint: Use `$project` + `$multiply` + `$floor`*)

✅ **Q3:** From the `comments` collection, show `email`, `movie_id`, and extract the year from the `date` field.

✅ **Q4:** For all movies, show `title` and `numberOfGenres`.

---

### 3. FAANG-Level Scenarios
- When should you use `$project` vs `$addFields` or `$set`?
- Can `$project` help reduce memory usage in the pipeline? Why?
- How does `$project` behave when used after `$unwind` or `$lookup`?

---

## 🔹 Topic 3: `$addFields` / `$set`  
🧠 (*They are **aliases** — do the same job: add or overwrite fields*)

blending in **arithmetic** and **string** operators, since `$addFields` is often where they are used.

---

### 1. Conceptual Questions
- What is the difference between `$addFields` and `$project`?
- When would you use `$addFields` over `$project`?
- Can `$addFields` access nested fields? Can it create them?
- Are `$addFields` fields immediately available to the next stage?

---

### 2. Hands-on with mflix (movies collection)

✅ **Q1:** Add a new field `isLongMovie` that is true if `runtime > 150`.

```js
db.movies.aggregate([
  {
    $addFields: {
      isLongMovie: { $gt: ["$runtime", 150] }
    }
  }
])
```

🧠 **Operators involved**: `$gt` (Comparison), `$addFields`

---

✅ **Q2:** Add a `titleLength` field using `$strLenCP`.

```js
db.movies.aggregate([
  {
    $addFields: {
      titleLength: { $strLenCP: "$title" }
    }
  }
])
```

🧠 **Operators involved**: `$strLenCP` (String), `$addFields`

---

✅ **Q3:** Add a `releaseDecade` field (e.g., 1990s, 2000s)

```js
db.movies.aggregate([
  {
    $addFields: {
      releaseDecade: {
        $concat: [
          { $toString: { $multiply: [{ $floor: { $divide: ["$year", 10] } }, 10] } },
          "s"
        ]
      }
    }
  }
])
```

🧠 **Operators involved**:
- `$floor`, `$divide`, `$multiply` (Arithmetic)
- `$toString`, `$concat` (String)

---

✅ **Q4:** Add a field `mainGenre` that picks the **first genre** from the array.

```js
db.movies.aggregate([
  {
    $addFields: {
      mainGenre: { $arrayElemAt: ["$genres", 0] }
    }
  }
])
```

🧠 **Operators involved**: `$arrayElemAt` (Array)

---

### 3. FAANG-Level Scenarios
- When using `$addFields`, what happens if the field already exists?
- What are the memory implications of using multiple `$addFields` vs combining into one?
- Can `$addFields` use computed values from previous `$project`? Why or why not?

---

## 🔹 Topic 4: `$unset`

> `$unset` is used to **remove one or more fields** from documents.  
Alias: `$project: { field: 0 }` does the same but `$unset` is more expressive.

---

### 1. Conceptual Questions
- What is the difference between `$unset` and excluding fields in `$project`?
- Can `$unset` remove nested fields like `meta.reviews.author`?
- Is `$unset` used only in `.aggregate()` or can it be used in `updateOne()`?

---

### 2. Hands-on with mflix (movies collection)

✅ **Q1:** Remove the field `poster` from all movie documents.
```js
db.movies.aggregate([
  { $unset: "poster" }
])
```

✅ **Q2:** Remove `plot`, `fullplot`, and `awards` from the output.
```js
db.movies.aggregate([
  { $unset: ["plot", "fullplot", "awards"] }
])
```

✅ **Q3:** Unset the nested field `tomatoes.viewer`.
```js
db.movies.aggregate([
  { $unset: "tomatoes.viewer" }
])
```

✅ **Q4:** Use in an **update pipeline**: Remove `awards` field from all movies released before 1990.
```js
db.movies.updateMany(
  { year: { $lt: 1990 } },
  [{ $unset: "awards" }]
)
```

---

### 3. FAANG-Level Scenarios
- When would you prefer `$unset` inside an `updateOne()` vs in `.aggregate()`?
- Can `$unset` help reduce document size and improve read performance?
- What happens if you try to `$unset` a non-existent field?

---

🧠 Operators implicitly involved:
- `$unset` interacts closely with document structure (Object Operators), updates, and schema optimization.

---

## 🔹 Topic 5: `$replaceWith`  
> Replaces the **entire document** with the specified expression. Super useful when reshaping deeply nested structures.

✅ Alias: `$replaceRoot`

---

### 1. Conceptual Questions

- What is the key difference between `$replaceWith` and `$project`?
- What happens if the expression in `$replaceWith` doesn’t return a full object?
- Can `$replaceWith` be used after `$lookup` to flatten nested data?

---

### 2. Hands-on with mflix (movies collection)

✅ **Q1:** Replace each document with the `tomatoes.viewer` sub-document (ratings object).

```js
db.movies.aggregate([
  { $match: { "tomatoes.viewer": { $exists: true } } },
  { $replaceWith: "$tomatoes.viewer" }
])
```

🧠 Good for: Flattening nested sub-docs

---

✅ **Q2:** Replace the root with a custom object containing `title`, `rating`, and computed `decade`.

```js
db.movies.aggregate([
  {
    $replaceWith: {
      $mergeObjects: [
        {
          title: "$title",
          rating: "$imdb.rating",
          decade: {
            $concat: [
              { $toString: { $multiply: [{ $floor: { $divide: ["$year", 10] } }, 10] } },
              "s"
            ]
          }
        }
      ]
    }
  }
])
```

🧠 Operators used:
- `$mergeObjects`, `$floor`, `$divide`, `$multiply`, `$toString`, `$concat`

---

✅ **Q3:** After a `$lookup`, replace the document root with an embedded review.

```js
db.movies.aggregate([
  {
    $lookup: {
      from: "comments",
      localField: "_id",
      foreignField: "movie_id",
      as: "comments"
    }
  },
  { $unwind: "$comments" },
  { $replaceWith: "$comments" }
])
```

🧠 Result: You now have a pipeline working *just* with comments.

---

### 3. FAANG-Level Scenarios
- When building microservices or analytics pipelines, how can `$replaceWith` reduce complexity of nested outputs?
- What happens to indexes and projections when you replace the full document?
- In what order should you use `$replaceWith`, `$lookup`, and `$unwind` to avoid performance pitfalls?

---

## 🔹 Topic 6: `$group`  
> Aggregates documents by a **_grouping key** (`_id`) and computes **accumulator expressions** like `$sum`, `$avg`, `$max`, `$push`, etc.

---

### 1. Conceptual Questions

- What is the purpose of `_id` in `$group`?
- What’s the difference between `$sum: 1` vs `$sum: "$someField"`?
- What are the limitations of using `$group` on large collections?
- Can you use `$group` after `$unwind` or `$lookup`?

---

### 2. Hands-on with mflix

✅ **Q1:** Group movies by `year`, count how many were released each year.

```js
db.movies.aggregate([
  {
    $group: {
      _id: "$year",
      movieCount: { $sum: 1 }
    }
  },
  { $sort: { _id: 1 } }
])
```

🧠 Operators: `$group`, `$sum`, `$sort`

---

✅ **Q2:** Group by `rated`, get **average IMDb rating** and **total movies per rating**.

```js
db.movies.aggregate([
  {
    $group: {
      _id: "$rated",
      avgRating: { $avg: "$imdb.rating" },
      totalMovies: { $sum: 1 }
    }
  },
  { $sort: { avgRating: -1 } }
])
```

🧠 Operators: `$avg`, `$sum`

---

✅ **Q3:** Group by decade and calculate the **highest box office grossing movie** (requires `$project` + `$group`)

```js
db.movies.aggregate([
  {
    $addFields: {
      decade: { $multiply: [{ $floor: { $divide: ["$year", 10] } }, 10] }
    }
  },
  {
    $group: {
      _id: "$decade",
      topBoxOffice: { $max: "$boxOffice" },
      movieTitles: { $push: "$title" }
    }
  }
])
```

---

✅ **Q4:** Group comments by `movie_id`, and count number of comments + last comment date.

```js
db.comments.aggregate([
  {
    $group: {
      _id: "$movie_id",
      commentCount: { $sum: 1 },
      latestComment: { $max: "$date" }
    }
  }
])
```

---

### 3. FAANG-Level Scenarios

- How can `$group` + `$project` + `$sort` build custom leaderboards or rankings?
- Why is it dangerous to use `$push` or `$addToSet` on massive datasets?
- What are streaming vs blocking stages in aggregation? Where does `$group` fall?

---

🧠 Bonus FAANG Insight:

- **Memory:** `$group` can spill to disk. Use `$limit`, `$sort`, or `$match` earlier to reduce memory usage.
- **Performance:** Always index grouping fields when possible if preceded by `$match`.

---

## 🔹 Topic 7: `$bucket`

> Categorizes documents into **explicit buckets** defined by **boundaries**  
(e.g., ratings 0–5, 5–7, 7–10). Great for **histograms** or **score bands**.

---

### 1. Conceptual Questions

- What happens to documents that fall **outside the defined range**?
- How do you handle documents **below the first boundary** or **above the last**?
- Can you use `$bucket` with `$lookup` or after `$group`?

---

### 2. Hands-on with mflix (movies)

✅ **Q1:** Bucket IMDb ratings into categories (0–5, 5–7, 7–10)

```js
db.movies.aggregate([
  {
    $match: { "imdb.rating": { $ne: null } }
  },
  {
    $bucket: {
      groupBy: "$imdb.rating",
      boundaries: [0, 5, 7, 10],
      default: "Other",
      output: {
        count: { $sum: 1 },
        titles: { $push: "$title" }
      }
    }
  }
])
```

🧠 Operators: `$bucket`, `$sum`, `$push`

---

✅ **Q2:** Bucket movies by **runtime** into 4 ranges and compute average IMDb rating in each.

```js
db.movies.aggregate([
  {
    $match: { runtime: { $exists: true } }
  },
  {
    $bucket: {
      groupBy: "$runtime",
      boundaries: [0, 60, 90, 120, 180],
      default: "Other",
      output: {
        avgRating: { $avg: "$imdb.rating" },
        count: { $sum: 1 }
      }
    }
  }
])
```

---

## 🔹 Topic 8: `$bucketAuto`

> Automatically creates **evenly distributed buckets** based on document count. You specify the **number of buckets**, not their boundaries.

---

### 3. Hands-on with `$bucketAuto`

✅ **Q3:** Auto-bucket movies based on IMDb rating into 5 groups

```js
db.movies.aggregate([
  {
    $match: { "imdb.rating": { $ne: null } }
  },
  {
    $bucketAuto: {
      groupBy: "$imdb.rating",
      buckets: 5,
      output: {
        count: { $sum: 1 },
        avgRuntime: { $avg: "$runtime" }
      }
    }
  }
])
```

---

### 4. FAANG-Level Challenges

- When should you prefer `$bucketAuto` over `$bucket`?
- Can you combine `$bucket` with `$facet` to show **multiple histograms** in one aggregation?
- How does `$bucketAuto` determine the boundaries internally?

---

💡 **Advanced Use Case**

Use `$bucketAuto` after `$project` or `$lookup` to analyze **user engagement score bands**, **product prices**, **review scores**, or **watch durations** dynamically.

---

## 🔹 Topic 9: `$sortByCount`

> A **shortcut** to get the **count** of distinct values for a field, followed by **sorting** the results. This is **super useful** when you're counting occurrences like most popular genres, frequent tags, or common ratings.

---

### 1. Conceptual Questions

- How does `$sortByCount` internally optimize the aggregation pipeline compared to `$group` and `$sort`?
- Can you use `$sortByCount` on fields with **nested objects** or arrays?
- What happens when there are **duplicate values** in the field you're counting?

---

### 2. Hands-on with mflix (movies collection)

✅ **Q1:** Get the **count** of each `genre` and sort them by the most popular.

```js
db.movies.aggregate([
  {
    $unwind: "$genres"
  },
  {
    $sortByCount: "$genres"
  }
])
```

🧠 This counts the occurrences of each genre in the dataset.

---

✅ **Q2:** Get the **count** of movies by `rated` value (e.g., PG, R, etc.)

```js
db.movies.aggregate([
  {
    $sortByCount: "$rated"
  }
])
```

---

✅ **Q3:** Get the **count** of all `directors` in the collection and sort by the most frequent.

```js
db.movies.aggregate([
  {
    $sortByCount: "$director"
  }
])
```

---

### 3. FAANG-Level Scenarios

- How can `$sortByCount` be useful for building **trending topic analysis** or **popularity metrics**?
- How would you handle large documents with deeply nested arrays (e.g., movie tags, keywords) when using `$sortByCount`?
- Is `$sortByCount` memory-efficient compared to `$group` + `$sort`?

---

💡 **Real-World Use Case:**
- Use `$sortByCount` to gather **top-viewed content** on a platform, **common user activities**, or **frequent search queries** for optimizing recommendations or reports.

---

## 🔹 Topic 10: `$count`

> The `$count` operator counts the **total number of documents** that reach this stage of the aggregation pipeline and returns it as a single document with the count.

---

### 1. Conceptual Questions

- How does `$count` compare to `$group` with `$sum: 1` in terms of performance?
- Can `$count` be used **before** `$group` to get a count of documents for some filtering condition?
- What is the output structure when using `$count`?

---

### 2. Hands-on with mflix (movies collection)

✅ **Q1:** Count the **total number of movies** in the collection.

```js
db.movies.aggregate([
  { $count: "totalMovies" }
])
```

🧠 This will return a single document with the field `totalMovies` and its value as the count of documents.

---

✅ **Q2:** Count movies released after the year 2000.

```js
db.movies.aggregate([
  { $match: { year: { $gt: 2000 } } },
  { $count: "moviesAfter2000" }
])
```

---

✅ **Q3:** Count the number of movies by each `rated` value (PG, R, etc.), but grouped first.

```js
db.movies.aggregate([
  {
    $group: {
      _id: "$rated"
    }
  },
  { $count: "ratedCount" }
])
```

---

### 3. FAANG-Level Scenarios

- When would you use `$count` after `$match` to **optimize query performance** on large datasets?
- Can `$count` be combined with `$facet` to get counts from different **sub-pipelines** simultaneously?
- How can `$count` assist in **pagination** strategies or **real-time analytics**?

---

💡 **Real-World Use Case:**
- Use `$count` for **reporting**, **summarizing data**, and creating **metrics** on the fly (e.g., number of purchases in a day, number of views for a video, or posts per category).

---

## 🔹 Topic 11: `$sort`

> The `$sort` operator sorts the documents based on one or more fields, either in **ascending** (`1`) or **descending** (`-1`) order. Essential for ranking, ordering results, and preparing data for presentation.

---

### 1. Conceptual Questions

- What happens if you **sort** on an **unindexed field**? 
- How does `$sort` affect the **performance** of the pipeline, especially on large datasets?
- Can you use `$sort` with **multiple fields**? If so, how do you prioritize the sort order?

---

### 2. Hands-on with mflix (movies collection)

✅ **Q1:** Sort the movies by `year` in **ascending order**.

```js
db.movies.aggregate([
  { $sort: { year: 1 } }
])
```

🧠 This sorts all movies from the **oldest** to the **newest**.

---

✅ **Q2:** Sort movies by `year` in **descending order**, and then by `title` in **ascending order**.

```js
db.movies.aggregate([
  { $sort: { year: -1, title: 1 } }
])
```

🧠 This sorts movies first by **year descending**, and then by **title ascending** within the same year.

---

✅ **Q3:** Sort movies based on **box office** in descending order and limit the top 5 highest-grossing films.

```js
db.movies.aggregate([
  { $sort: { boxOffice: -1 } },
  { $limit: 5 }
])
```

---

### 3. FAANG-Level Scenarios

- What are the potential **downsides** of using `$sort` on an **unindexed field**? How would you mitigate that in a production environment?
- If the pipeline contains multiple `$sort` stages, what are the **best practices** for ordering them? Does the order matter?
- How would you **optimize the sorting** of data when working with **millions of records** in a production database (considering performance)?

---

💡 **Real-World Use Case:**
- Use `$sort` to **rank results** (e.g., top-rated products, latest movies, best-selling items) and **prepare the data** for reports or dashboards.
- Combine `$sort` with `$limit` for **pagination** or displaying **top N results**.

---

## 🔹 Topic 12: `$limit`

> The `$limit` operator restricts the number of documents passed along to the next stage of the aggregation pipeline. It’s essential for **pagination**, **sampling**, and limiting large result sets.

---

### 1. Conceptual Questions

- How does `$limit` interact with the rest of the pipeline, particularly stages like `$sort` or `$skip`?
- Can `$limit` be combined with `$sort` to ensure that you get the **most recent**, **highest-rated**, or **top N** documents?
- What are the performance implications when applying `$limit` on **large collections** or **complex pipelines**?

---

### 2. Hands-on with mflix (movies collection)

✅ **Q1:** Get the **top 5 most recent movies** based on `year`.

```js
db.movies.aggregate([
  { $sort: { year: -1 } },
  { $limit: 5 }
])
```

🧠 This returns the most **recent** 5 movies based on the `year` field.

---

✅ **Q2:** Get the **top 3 highest-rated movies** based on `imdb.rating`.

```js
db.movies.aggregate([
  { $sort: { "imdb.rating": -1 } },
  { $limit: 3 }
])
```

---

✅ **Q3:** Get the **first 10 movies** released after 2010, sorted by `year`.

```js
db.movies.aggregate([
  { $match: { year: { $gt: 2010 } } },
  { $sort: { year: 1 } },
  { $limit: 10 }
])
```

---

### 3. FAANG-Level Scenarios

- How can `$limit` help when building APIs that require **pagination** (e.g., REST APIs, GraphQL)?
- In large datasets, how would you combine `$limit` with `$skip` for **efficient pagination**?
- If you're building a **real-time application** where results are frequently updated, how would you apply `$limit` to ensure **fresh data**?

---

💡 **Real-World Use Case:**
- Use `$limit` to fetch **top N results** (e.g., top-rated movies, popular products, most viewed content) for quick user display or ranking purposes. Combine it with `$skip` for **pagination** (especially in APIs or UI).

---

## 🔹 Topic 13: `$skip`

> The `$skip` operator skips over a specified number of documents in the aggregation pipeline. This is extremely useful for **pagination** or **offsetting results** when combined with `$limit`.

---

### 1. Conceptual Questions

- How does `$skip` work in conjunction with `$limit` to implement **pagination** effectively?
- What happens if you use `$skip` with **sorted data**? Does it affect the order of the results?
- Does `$skip` consume memory or resources differently than other aggregation stages (like `$match` or `$group`)?

---

### 2. Hands-on with mflix (movies collection)

✅ **Q1:** Skip the first 5 movies and then get the **next 5** most recent movies based on `year`.

```js
db.movies.aggregate([
  { $sort: { year: -1 } },
  { $skip: 5 },
  { $limit: 5 }
])
```

🧠 This skips the first 5 movies and returns the next 5 movies in descending order by `year`.

---

✅ **Q2:** Skip the first 10 movies released after 2010 and get the next 10.

```js
db.movies.aggregate([
  { $match: { year: { $gt: 2010 } } },
  { $sort: { year: 1 } },
  { $skip: 10 },
  { $limit: 10 }
])
```

---

✅ **Q3:** Skip 100 movies from the `genres` field, then return the **next 10** with a specific genre.

```js
db.movies.aggregate([
  { $match: { genres: "Comedy" } },
  { $skip: 100 },
  { $limit: 10 }
])
```

---

### 3. FAANG-Level Scenarios

- How does the **combination of `$skip` and `$limit`** allow you to implement **pagination** efficiently, and how does this improve user experience?
- In a **real-time system**, how would `$skip` be affected by frequent updates to the collection? How would you ensure you're still retrieving the correct "next" set of documents?
- If a dataset is very large, how can you optimize the performance of `$skip`? Should you use **indexes** on frequently queried fields?

---

💡 **Real-World Use Case:**
- Use `$skip` and `$limit` in combination for **pagination** in REST APIs or GraphQL queries (e.g., displaying 20 movies per page or loading content in infinite scroll).

## 🔹 Topic 14: `$unwind`

> The `$unwind` operator deconstructs an array field from the documents and creates a separate document for each element in that array. This is perfect for working with nested data where you want to analyze or manipulate each element individually.

---

### 1. Conceptual Questions

- What happens if the array you’re unwinding is **empty** or **missing** from a document?
- How can `$unwind` help in situations where you need to **flatten nested arrays** for easier querying or aggregation?
- How does `$unwind` affect the **number of documents** in the pipeline, and how does it impact performance?

---

### 2. Hands-on with mflix (movies collection)

✅ **Q1:** Unwind the `genres` array to get a document for each genre for every movie.

```js
db.movies.aggregate([
  { $unwind: "$genres" }
])
```

🧠 This creates a separate document for each genre of the movie, which is useful if you want to analyze the frequency of each genre in the collection.

---

✅ **Q2:** Unwind the `cast` array and then group the actors by the number of movies they've appeared in.

```js
db.movies.aggregate([
  { $unwind: "$cast" },
  { $group: { _id: "$cast", movieCount: { $sum: 1 } } },
  { $sort: { movieCount: -1 } }
])
```

---

✅ **Q3:** Unwind the `comments` array and find the **average rating** for each comment in the array (assuming `comments.rating` exists).

```js
db.movies.aggregate([
  { $unwind: "$comments" },
  { $group: { _id: "$comments.user", avgRating: { $avg: "$comments.rating" } } }
])
```

---

### 3. FAANG-Level Scenarios

- How would you handle **arrays with null or empty values** in `$unwind`? Can you use `$unwind` with an `optional` flag to exclude empty arrays?
- If you have a **nested array of arrays**, how would you use `$unwind` in **multiple stages** to flatten the structure progressively?
- What are the **performance considerations** when working with large arrays, especially when unwinding multiple fields?

---

💡 **Real-World Use Case:**
- Use `$unwind` for **flattening reviews, tags, comments**, or **nested user actions** in applications like e-commerce platforms, social media, or content management systems. This allows you to analyze individual elements more effectively.

---

## 🔹 Topic 15: `$lookup`

> The `$lookup` operator allows you to join two collections, essentially performing a **left outer join** between documents in the current collection and another collection, based on a common field. This is crucial for combining related data spread across multiple collections.

---

### 1. Conceptual Questions

- How does `$lookup` differ from traditional **SQL joins** in terms of functionality and performance?
- What happens if the field you're joining on is **indexed** versus **not indexed**?
- How can `$lookup` be optimized when dealing with **large datasets** or **complex joins**?

---

### 2. Hands-on with mflix (movies and directors collections)

✅ **Q1:** Perform a lookup to find the **directors** for each movie by joining the `movies` collection with a `directors` collection based on the `director_id`.

```js
db.movies.aggregate([
  { $lookup: {
    from: "directors",          // The collection to join
    localField: "director_id",   // The field from the current collection
    foreignField: "_id",         // The field from the "from" collection
    as: "director_info"          // The field to store the joined data
  }}
])
```

🧠 This will add a `director_info` field to each movie document, containing the director’s details.

---

✅ **Q2:** Join the `movies` collection with `cast` information based on the actor's `actor_id`.

```js
db.movies.aggregate([
  { $lookup: {
    from: "cast", 
    localField: "cast_id", 
    foreignField: "_id", 
    as: "cast_info"
  }}
])
```

---

✅ **Q3:** Perform a lookup and then filter movies based on a **specific director's name** using `$match`.

```js
db.movies.aggregate([
  { $lookup: {
    from: "directors",
    localField: "director_id",
    foreignField: "_id",
    as: "director_info"
  }},
  { $unwind: "$director_info" },
  { $match: { "director_info.name": "Christopher Nolan" } }
])
```

---

### 3. FAANG-Level Scenarios

- What would happen if you tried to use `$lookup` on an **unindexed field**? How can this degrade performance when joining large datasets, and how would you optimize it?
- How would you handle cases where there is **no matching document** in the second collection? Would you use `$lookup` with a **default value** in such cases?
- How would you deal with **nested fields** in the result set from `$lookup` and manipulate them using other aggregation operators?

---

💡 **Real-World Use Case:**
- Use `$lookup` to **join related data** from multiple collections, such as joining user data with their orders, joining product details with categories, or merging movie information with director and cast details.

---

## 🔹 Topic 16: `$graphLookup`

> The `$graphLookup` operator allows you to perform a **recursive search** within the same collection to retrieve related documents, useful for hierarchical or graph-like data (e.g., organizational charts, folder structures, etc.).

---

### 1. Conceptual Questions

- How does `$graphLookup` differ from `$lookup` in terms of its ability to handle **recursive relationships**?
- What happens if there are **cyclic dependencies** in the data being traversed with `$graphLookup`? How do you avoid infinite loops?
- How does `$graphLookup` handle **performance** when working with very deep or complex hierarchies?

---

### 2. Hands-on with mflix (movies collection)

✅ **Q1:** Perform a graph lookup to find **all movies related to a specific movie**, based on a `related_movie_id` field that references other movies in the same collection.

```js
db.movies.aggregate([
  { $graphLookup: {
    from: "movies",
    startWith: "$related_movie_id",  // Field in current collection
    connectFromField: "related_movie_id", // Field to connect in the starting collection
    connectToField: "_id",  // Field to connect to in the "from" collection
    as: "related_movies",   // Field where the results will be stored
    maxDepth: 5,            // Limits the recursion depth to 5
    depthField: "depth"     // Field to track the depth level
  }}
])
```

🧠 This will recursively find related movies up to a depth of 5.

---

✅ **Q2:** Get all movies in a specific **genre** (assuming movies have `genre` and `related_genre_id` fields) by recursively finding movies within the same genre.

```js
db.movies.aggregate([
  { $match: { genre: "Action" } },
  { $graphLookup: {
    from: "movies",
    startWith: "$related_genre_id",
    connectFromField: "related_genre_id",
    connectToField: "genre",
    as: "related_genre_movies",
    maxDepth: 3
  }}
])
```

---

✅ **Q3:** Find all **subordinate employees** in an organizational structure (assuming we have an `employees` collection with fields like `employee_id`, `manager_id`).

```js
db.employees.aggregate([
  { $graphLookup: {
    from: "employees",
    startWith: "$employee_id",
    connectFromField: "employee_id",
    connectToField: "manager_id",
    as: "subordinates",
    maxDepth: 5,
    depthField: "level"
  }}
])
```

---

### 3. FAANG-Level Scenarios

- How can you handle **cyclic references** in your data when using `$graphLookup` (e.g., a recursive reference in a hierarchical structure)?
- In complex recursive queries, how can you **optimize performance** and avoid hitting **memory limits**?
- When working with recursive graphs, how do you handle **depth limitation** and ensure that you don't return **infinite loops**?

---

💡 **Real-World Use Case:**
- Use `$graphLookup` to traverse **parent-child relationships** (e.g., folder structures, employee-manager relationships), or find **all related content** in a **content recommendation system** (movies, articles, etc.).

---

## 🔹 Topic 17: `$unionWith`

> The `$unionWith` operator is used to combine the results of two collections into a **single result set**. This operation is similar to a **union** in SQL, where duplicate documents are automatically removed, and the results are merged.

---

### 1. Conceptual Questions

- How does `$unionWith` differ from `$lookup` when combining data from two collections?
- What happens if the two collections being merged have different **schemas** or field names? How do you handle such cases?
- When would you use `$unionWith` over `$lookup` for merging data from different collections?

---

### 2. Hands-on with mflix (movies and ratings collections)

✅ **Q1:** Combine the **movies** and **ratings** collections to create a list of all **movies** and their ratings. Assume both collections share a `movie_id` field.

```js
db.movies.aggregate([
  { $unionWith: {
    coll: "ratings",    // The second collection to merge with
    pipeline: [         // Pipeline to process the second collection before union
      { $project: { movie_id: 1, rating: 1 } }
    ]
  }}
])
```

🧠 This will merge all documents from `movies` with the ratings data, keeping the necessary fields.

---

✅ **Q2:** Combine two collections, `movies` and `actors`, where both collections have an `actor_id` field, and get a list of all **actors** and their associated **movies**.

```js
db.movies.aggregate([
  { $unionWith: {
    coll: "actors",
    pipeline: [
      { $project: { actor_id: 1, movie_id: 1, name: 1 } }
    ]
  }}
])
```

---

✅ **Q3:** Combine the **movies** and **reviews** collections, and filter the results to show only movies released after 2010.

```js
db.movies.aggregate([
  { $match: { year: { $gt: 2010 } } },
  { $unionWith: {
    coll: "reviews",
    pipeline: [
      { $project: { movie_id: 1, review: 1, year: 1 } }
    ]
  }}
])
```

---

### 3. FAANG-Level Scenarios

- How do you handle cases where the **field names** in the two collections you are merging do not match? How do you ensure compatibility before performing a union?
- When merging two collections, how would you **filter out duplicates** that might appear after the union (in case of overlapping documents)?
- How would you ensure **optimal performance** when using `$unionWith` on very large collections, particularly in a **real-time system**?

---

💡 **Real-World Use Case:**
- Use `$unionWith` to merge **data from multiple sources** (e.g., combining product data from different APIs, merging **user activity logs** from multiple services, or combining **user-generated content** with system-generated content).

---

## 🔹 Topic 18: `$facet`

> The `$facet` operator allows you to run multiple aggregation pipelines **in parallel** within the same query, and outputs the results as separate fields in a single document. It’s useful for generating multiple views or analyses of the same dataset simultaneously.

---

### 1. Conceptual Questions

- How does `$facet` help in running **multiple aggregation pipelines** at once, and why is it more efficient than running them sequentially?
- What happens if the **sub-pipelines** inside a `$facet` have different data requirements or **scopes**? How do you handle this?
- How does `$facet` **affect the performance** when aggregating large datasets, and what are the potential bottlenecks?

---

### 2. Hands-on with mflix (movies collection)

✅ **Q1:** Use `$facet` to get the **total number of movies** and the **average rating** for all movies in the `movies` collection.

```js
db.movies.aggregate([
  { $facet: {
    totalMovies: [{ $count: "total" }],
    averageRating: [{ $group: { _id: null, avgRating: { $avg: "$rating" } } }]
  }}
])
```

🧠 This aggregates the total count of movies and the average rating in a single query, with both results output in different fields (`totalMovies` and `averageRating`).

---

✅ **Q2:** Use `$facet` to calculate both the **total number of movies** and the **top 5 most popular genres** based on the number of movies in each genre.

```js
db.movies.aggregate([
  { $facet: {
    totalMovies: [{ $count: "total" }],
    topGenres: [
      { $unwind: "$genres" },
      { $group: { _id: "$genres", count: { $sum: 1 } } },
      { $sort: { count: -1 } },
      { $limit: 5 }
    ]
  }}
])
```

---

✅ **Q3:** Use `$facet` to generate multiple views: one showing the total count of movies, one showing the average rating, and another showing the movies released after 2015.

```js
db.movies.aggregate([
  { $facet: {
    totalMovies: [{ $count: "total" }],
    avgRating: [{ $group: { _id: null, avgRating: { $avg: "$rating" } } }],
    recentMovies: [{ $match: { year: { $gt: 2015 } } }]
  }}
])
```

---

### 3. FAANG-Level Scenarios

- How would you deal with **large data sets** in `$facet` where some pipelines might return a very high number of documents? What strategies would you employ to handle **data size limitations**?
- If you need to **optimize performance** for complex `$facet` operations, how would you use **indexes** and **limit operators** to minimize the data processed?
- Can you combine `$facet` with other operators like `$sort`, `$limit`, or `$skip` within the sub-pipelines, and how would this affect the resulting data?

---

💡 **Real-World Use Case:**
- Use `$facet` when you need to generate **multiple reports or statistics** in a single query, such as **user activity insights**, **e-commerce sales reports**, or **social media analysis**.

---

## 🔹 Topic 19: `$sample`

> The `$sample` operator is used to **randomly select a specified number of documents** from a collection. This is useful for sampling data when you need to process a subset of your data randomly, such as for creating randomized tests, building recommendation systems, or conducting A/B testing.

---

### 1. Conceptual Questions

- How does `$sample` ensure the randomness of the documents it selects? Is there any performance impact when sampling a large number of documents from a large collection?
- How does `$sample` compare to using `$limit` in terms of selecting a subset of data?
- What are some real-world scenarios where `$sample` would be **beneficial** as compared to other methods of filtering or selecting documents?

---

### 2. Hands-on with mflix (movies collection)

✅ **Q1:** Randomly select **5 movies** from the `movies` collection.

```js
db.movies.aggregate([
  { $sample: { size: 5 } }
])
```

🧠 This will return 5 random movies from the collection.

---

✅ **Q2:** Randomly select **10 documents** from the `reviews` collection, where the `rating` is greater than 4.

```js
db.reviews.aggregate([
  { $match: { rating: { $gt: 4 } } },
  { $sample: { size: 10 } }
])
```

---

✅ **Q3:** Use `$sample` to randomly select **1 document** from the `movies` collection and then get its **related movies** using `$graphLookup`.

```js
db.movies.aggregate([
  { $sample: { size: 1 } },
  { $graphLookup: {
    from: "movies",
    startWith: "$related_movie_id",
    connectFromField: "related_movie_id",
    connectToField: "_id",
    as: "related_movies",
    maxDepth: 2
  }}
])
```

---

### 3. FAANG-Level Scenarios

- How would you ensure that `$sample` gives you a truly **random sample** when working with highly skewed data, where certain documents are more likely to appear?
- In a scenario with millions of documents, how do you handle the **performance overhead** of using `$sample`? What strategies do you employ to improve efficiency?
- If you need to **adjust the randomness** (e.g., to ensure different sampling distributions), what alternatives or modifications to `$sample` would you consider?

---

💡 **Real-World Use Case:**
- Use `$sample` to generate **random test cases**, **recommendation systems** (randomly select movies, products, or users), or **A/B testing** for randomized experiments.

---

## 🔹 Topic 20: `$setWindowFields`

> The `$setWindowFields` operator allows you to perform **window operations** across documents within a specified "window" or group. This is useful for operations like **ranking, running totals**, or calculating **moving averages** over documents, much like window functions in SQL.

---

### 1. Conceptual Questions

- What is the role of the **"window"** in the `$setWindowFields` operator? How does it differ from a simple group or aggregation operation?
- How does `$setWindowFields` handle **document ordering** within the window? What happens if documents are not ordered appropriately?
- In what scenarios would you use `$setWindowFields` over other aggregation methods like `$group`, `$sort`, or `$bucket`?

---

### 2. Hands-on with mflix (movies collection)

✅ **Q1:** Rank movies based on their **rating** in descending order, with each movie getting a **rank** number.

```js
db.movies.aggregate([
  { $setWindowFields: {
    sortBy: { rating: -1 },
    output: {
      rank: { $rank: {} }
    }
  }}
])
```

🧠 This will assign a rank to each movie based on its rating, starting from 1 for the highest rating.

---

✅ **Q2:** Calculate a **running total** of the `box_office` field for the `movies` collection, ordered by the release year.

```js
db.movies.aggregate([
  { $setWindowFields: {
    sortBy: { year: 1 },
    output: {
      runningTotal: { $sum: "$box_office" }
    }
  }}
])
```

---

✅ **Q3:** Calculate the **moving average rating** of movies over the past 5 years.

```js
db.movies.aggregate([
  { $setWindowFields: {
    sortBy: { year: 1 },
    output: {
      movingAvgRating: {
        $avg: "$rating",
        window: { documents: [-5, 0] }  // Includes the previous 5 documents and the current one
      }
    }
  }}
])
```

---

### 3. FAANG-Level Scenarios

- How do you handle **partitioning** documents across multiple groups when performing window operations? Can you partition by a field like `genre` or `director` to calculate rankings or totals within each genre or director group?
- In a large-scale application, how would you optimize the use of `$setWindowFields` to ensure that window operations do not **overwhelm the system** in terms of memory and processing time?
- Can `$setWindowFields` be combined with other operators (like `$group`, `$facet`, etc.) for more complex aggregations? If so, how would you do that efficiently?

---

💡 **Real-World Use Case:**
- Use `$setWindowFields` in a **financial application** to compute running totals, moving averages, or to rank stocks based on performance over time.
- For **content platforms**, you can use it to **rank users** by activity level, or **rank movies** based on popularity or view counts.

---

## 🔹 Topic 21: `$geoNear`

> The `$geoNear` operator is used for **geospatial queries** and finds documents that are closest to a specified point. It is useful for searching locations near a specific coordinate, such as finding nearby restaurants, stores, or events.

---

### 1. Conceptual Questions

- How does `$geoNear` differ from other geospatial queries, such as `$near` or `$geoWithin`? When would you specifically use `$geoNear`?
- What are the requirements for using `$geoNear`? How do you ensure that your collection is **indexed correctly** for efficient geospatial queries?
- What happens if the point specified in `$geoNear` is **out of bounds** or the location does not match any documents in the collection?

---

### 2. Hands-on with mflix (movies collection)

✅ **Q1:** Find the **5 nearest theaters** (represented by coordinates in a `location` field) to a specified point (latitude: 40.730610, longitude: -73.935242).

```js
db.theaters.createIndex({ location: "2dsphere" });  // Ensure the geospatial index is created

db.theaters.aggregate([
  { $geoNear: {
    near: { type: "Point", coordinates: [-73.935242, 40.730610] },
    distanceField: "dist.calculated",
    maxDistance: 5000,  // Limit the search to theaters within 5 km
    spherical: true,
    limit: 5
  }}
])
```

🧠 This query will return the 5 nearest theaters to the specified coordinates.

---

✅ **Q2:** Find all movies that are being shown within **50 km** of a specific theater (specified by its `location` field).

```js
db.movies.aggregate([
  { $geoNear: {
    near: { type: "Point", coordinates: [-73.935242, 40.730610] },
    distanceField: "dist.calculated",
    maxDistance: 50000,  // 50 km radius
    spherical: true
  }}
])
```

---

✅ **Q3:** Retrieve the **10 closest theaters** to a given user location, sorted by distance.

```js
db.theaters.aggregate([
  { $geoNear: {
    near: { type: "Point", coordinates: [-73.935242, 40.730610] },
    distanceField: "dist.calculated",
    spherical: true,
    limit: 10
  }},
  { $sort: { "dist.calculated": 1 } }
])
```

---

### 3. FAANG-Level Scenarios

- How do you handle **performance issues** when using `$geoNear` on a large-scale dataset (millions of documents)? Would you use **caching** or **pre-aggregation** to improve speed?
- How would you implement **user-specific geospatial queries**, like finding **nearest locations to a user’s current position**? What considerations would you have in terms of **accuracy**, **data freshness**, and **scalability**?
- What strategies would you use to prevent **out of bounds** errors or **empty results** when performing `$geoNear` queries, especially in cases where the user's location may be in an area with no nearby documents?

---

💡 **Real-World Use Case:**
- Use `$geoNear` for location-based apps such as **ride-hailing services**, **food delivery**, or **event discovery** platforms to find the nearest available options (e.g., drivers, restaurants, theaters) to a user's location.

---

## 🔹 Topic 22: `$collStats`

> The `$collStats` operator provides **statistics about a collection**. This includes information like the number of documents, storage size, and index statistics. It's useful for performance analysis, monitoring, and optimization of your MongoDB collections.

---

### 1. Conceptual Questions

- What kind of **statistics** can you retrieve using `$collStats`? How can these statistics help in **performance tuning** and optimizing queries?
- How does `$collStats` compare to other methods of gathering database performance data, such as using **`db.stats()`** or **`explain()`**?
- What are the potential **overheads** of running `$collStats` on a very large collection? How does it affect the system’s performance?

---

### 2. Hands-on with mflix (movies collection)

✅ **Q1:** Retrieve basic statistics about the `movies` collection (such as document count, storage size, and index details).

```js
db.movies.aggregate([
  { $collStats: { latencyStats: { intervalMs: 1000 } } }
])
```

🧠 This will return statistics on the collection, including query and write latency.

---

✅ **Q2:** Get **detailed statistics** of the `reviews` collection, including the size of the data and the indexes being used.

```js
db.reviews.aggregate([
  { $collStats: { count: true, storageSize: true, indexDetails: true } }
])
```

---

### 3. FAANG-Level Scenarios

- How would you incorporate `$collStats` data into your **performance monitoring** pipeline for MongoDB? What other tools would you combine it with to get a **holistic view** of your database’s health and performance?
- Given that `$collStats` provides detailed statistics, how would you use this information to **optimize your collection’s schema** or **indexing strategy** for performance-critical applications (e.g., real-time data feeds)?
- How do you mitigate the **impact of `$collStats` on a live production system** when used in a high-traffic environment with large datasets?

---

💡 **Real-World Use Case:**
- Use `$collStats` to **track collection growth** and identify performance bottlenecks, such as whether specific indexes need to be adjusted or if certain collections are consuming too much storage or causing latency issues.

---

## 🔹 Topic 23: `$indexStats`

> The `$indexStats` operator provides **statistics about the indexes** of a collection, such as how often each index is used and how much memory it consumes. This is useful for understanding the **effectiveness** of your indexes and making data-driven decisions for optimization.

---

### 1. Conceptual Questions

- What kind of **index-related statistics** can you retrieve using `$indexStats`? How can these statistics inform decisions about which indexes to optimize or drop?
- How does `$indexStats` help with **identifying unused indexes** and improving **query performance**? What impact does it have on **disk space** and **memory** usage?
- What are the potential **performance issues** when querying `$indexStats` on a collection with numerous indexes? How do you handle large-scale collections effectively?

---

### 2. Hands-on with mflix (movies collection)

✅ **Q1:** Get the **index usage statistics** for the `movies` collection. This will show how often each index has been used.

```js
db.movies.aggregate([
  { $indexStats: {} }
])
```

🧠 This query will provide the index usage statistics, including the **name of each index** and how often it has been used for queries.

---

✅ **Q2:** Retrieve the **size of each index** and how much memory it is consuming in the `movies` collection.

```js
db.movies.aggregate([
  { $indexStats: { indexDetails: true } }
])
```

---

✅ **Q3:** Get **detailed statistics** for all indexes in the `reviews` collection, and filter out those that have not been used.

```js
db.reviews.aggregate([
  { $indexStats: {} },
  { $match: { "accesses.ops": { $gt: 0 } } }  // Filter indexes that have been used at least once
])
```

---

### 3. FAANG-Level Scenarios

- How would you utilize `$indexStats` in a **performance audit** of your MongoDB deployment? What insights would you look for to identify **underused indexes** or potential **index bloat**?
- If you discover that certain indexes are **seldom used**, how would you **reassess** or **rebuild** your indexing strategy for improved query performance and reduced storage overhead?
- How would you automate the use of `$indexStats` in a **monitoring system** to flag **index performance issues** over time, especially for collections with high read/write volumes?

---

💡 **Real-World Use Case:**
- Use `$indexStats` to **optimize indexes** by identifying unused or inefficient indexes, which can be dropped to improve performance or rebuilt for more efficient queries.

---

## 🔹 Topic 24: `$redact`

> The `$redact` operator is used to **filter document fields** based on conditions. It allows for **fine-grained control** over which fields are included or excluded in the aggregation pipeline, depending on a condition or logic. This can be useful for **data privacy** or filtering sensitive information.

---

### 1. Conceptual Questions

- How does `$redact` differ from other operators like `$project` or `$addFields`? What makes it useful for complex field-level **data filtering**?
- What are the possible **performance concerns** when using `$redact`? How does it affect the overall execution of the aggregation pipeline?
- How would you use `$redact` to implement **role-based access control (RBAC)** in an application, ensuring that different users can see different data fields?

---

### 2. Hands-on with mflix (movies collection)

✅ **Q1:** Redact the `cast` field in the `movies` collection so that only specific roles (e.g., **admin**) can see the full cast list, while others see a **partial cast list**.

```js
db.movies.aggregate([
  { $redact: {
    $cond: {
      if: { $eq: ["$role", "admin"] },  // Check if the user is an admin
      then: "$$KEEP",  // Keep the full cast field for admins
      else: { $slice: ["$cast", 3] }  // Only show the first 3 actors for non-admins
    }
  }}
])
```

🧠 This will redact the `cast` field based on the user's role, allowing admins to see the full list and regular users to see only the first 3 actors.

---

✅ **Q2:** Redact the `ratings` field in the `movies` collection based on a condition, where only movies with a rating **greater than or equal to 7** will show their rating.

```js
db.movies.aggregate([
  { $redact: {
    $cond: {
      if: { $gte: ["$rating", 7] },
      then: "$$KEEP",  // Keep the rating field for movies with a rating >= 7
      else: "$$PRUNE"   // Remove the rating field for movies with a rating < 7
    }
  }}
])
```

---

✅ **Q3:** Implement a filter on the `reviews` collection so that users can see the review content only if their **subscription level** is **premium**.

```js
db.reviews.aggregate([
  { $redact: {
    $cond: {
      if: { $eq: ["$subscriptionLevel", "premium"] },
      then: "$$KEEP",  // Keep the review content for premium users
      else: "$$PRUNE"   // Remove the review content for non-premium users
    }
  }}
])
```

---

### 3. FAANG-Level Scenarios

- How would you implement **fine-grained data filtering** in a **multi-tenant application** using `$redact`, ensuring that tenants only see their own data and not others?
- If `$redact` introduces performance bottlenecks, how would you optimize its usage, especially on large collections or high-traffic systems?
- How would you **combine `$redact` with other aggregation operators** like `$match` or `$group` for more complex data filtering scenarios (e.g., filtering based on business rules or access rights)?

---

💡 **Real-World Use Case:**
- Use `$redact` in a **financial application** to redact sensitive information like **bank account numbers** or **transaction amounts** based on the **user's role** or **access rights**. Only allow specific roles (e.g., admins) to see full transaction details.

---

## 🔹 Topic 25: `$planCacheStats`

> The `$planCacheStats` operator provides **statistics about query plans** that are cached for a collection. It helps identify which query plans are being used, how often, and whether they are optimal. This is useful for debugging and optimizing queries, particularly in **performance tuning** and **caching strategies**.

---

### 1. Conceptual Questions

- What types of **query plan statistics** can you retrieve using `$planCacheStats`? How do these statistics help in identifying **inefficient queries** or **suboptimal plans**?
- How does the **query plan cache** work in MongoDB, and what role does `$planCacheStats` play in **monitoring** the effectiveness of cached query plans?
- How do you clear or **invalidate the plan cache** to force MongoDB to reevaluate query plans?

---

### 2. Hands-on with mflix (movies collection)

✅ **Q1:** Retrieve the **plan cache statistics** for the `movies` collection to see how many times query plans have been used.

```js
db.movies.aggregate([
  { $planCacheStats: {} }
])
```

🧠 This will give you statistics about the query plans that have been cached for the `movies` collection.

---

✅ **Q2:** Get the **top query plans** from the plan cache, including their execution count, and identify the most frequently used ones.

```js
db.movies.aggregate([
  { $planCacheStats: { queryPlans: { top: 5 } } }
])
```

---

✅ **Q3:** Find the **stale or inefficient** query plans by filtering the statistics based on their **execution time** or **hit counts**.

```js
db.movies.aggregate([
  { $planCacheStats: {} },
  { $match: { "planCacheStats.executionCount": { $lt: 100 } } } // Filter for less frequent plans
])
```

---

### 3. FAANG-Level Scenarios

- How would you leverage `$planCacheStats` in a **production environment** to continuously monitor and **optimize query performance**, especially as the dataset grows and query patterns evolve over time?
- If you discover that a certain query plan is **inefficient** or **rarely used**, what actions would you take to **optimize** the query or adjust indexing strategies to make the query plan more effective?
- In cases where MongoDB keeps generating suboptimal plans for a specific query, how could `$planCacheStats` help identify the root cause, and what steps would you take to resolve the issue?

---

💡 **Real-World Use Case:**
- Use `$planCacheStats` to **monitor and analyze** the effectiveness of your query plans over time, particularly for complex or frequent queries. If certain queries are consistently using inefficient plans, you can revisit indexing strategies or rewrite queries to improve performance.

---

## 🔹 Topic 26: `$merge`

> The `$merge` operator is used to **merge the results of an aggregation pipeline into another collection**. This allows you to save or update the results of an aggregation into a new or existing collection, making it an essential tool for scenarios like **data transformation** or **ETL (Extract, Transform, Load)** operations.

---

### 1. Conceptual Questions

- How does the `$merge` operator differ from the `$out` operator, and when would you choose one over the other?
- What are the **different modes** available for `$merge` (e.g., **merge**, **replace**, **keepExisting**, **failOnError**), and how do they affect the behavior of the operation?
- How do you handle **data conflicts** when using `$merge` in a **concurrent environment** where multiple processes might be attempting to update the same target collection?

---

### 2. Hands-on with mflix (movies collection)

✅ **Q1:** Merge the aggregation results into a new collection called `movies_summary` that contains only the movie title and average rating.

```js
db.movies.aggregate([
  { $group: { _id: "$title", averageRating: { $avg: "$rating" } } },
  { $merge: { into: "movies_summary" } }
])
```

🧠 This will aggregate the `movies` collection to calculate the average rating per movie and store the results in a new collection `movies_summary`.

---

✅ **Q2:** Merge the aggregation results into an **existing collection**, updating only the movies with a new field `lastUpdated`, indicating when they were aggregated.

```js
db.movies.aggregate([
  { $project: { title: 1, lastUpdated: new Date() } },
  { $merge: { into: "movies", whenMatched: "merge", whenNotMatched: "insert" } }
])
```

---

✅ **Q3:** Use `$merge` with the **failOnError** option to ensure that the merge operation fails if any errors occur.

```js
db.movies.aggregate([
  { $group: { _id: "$director", movieCount: { $sum: 1 } } },
  { $merge: { into: "directors_summary", failOnError: true } }
])
```

---

### 3. FAANG-Level Scenarios

- How would you use `$merge` in an **ETL pipeline** where you are transforming data from one collection into another? What considerations do you need to make when choosing between `replace`, `merge`, and other modes?
- In a scenario where you are dealing with **real-time data updates**, how would you ensure that `$merge` doesn’t overwrite or conflict with concurrent writes to the target collection?
- How would you design an **automated backup** solution using `$merge`, where results of certain aggregation queries (like monthly summaries) are merged into backup collections?

---

💡 **Real-World Use Case:**
- Use `$merge` in **reporting or data warehousing** systems to aggregate data and periodically update summary statistics in separate collections, optimizing query performance without impacting the main transactional database.

---

## 🔹 Topic 27: `$out`

> The `$out` operator is similar to `$merge` but with a key difference: it **replaces the entire target collection** with the results of the aggregation pipeline. This is useful when you need to **overwrite** a collection with freshly aggregated data, such as in **batch processing** or **data warehousing** tasks.

---

### 1. Conceptual Questions

- How does `$out` differ from `$merge`, particularly in terms of **collection replacement** and **data persistence**?
- What happens if the target collection in `$out` already exists? How can this affect your data, and why would this be useful or problematic in certain scenarios?
- Can `$out` be used in **sharded clusters**, and what are the **limitations** of using `$out` in a sharded environment?

---

### 2. Hands-on with mflix (movies collection)

✅ **Q1:** Use `$out` to **create a new collection** `top_rated_movies` containing only movies with a rating greater than or equal to 8. This collection will be created from the aggregation results.

```js
db.movies.aggregate([
  { $match: { rating: { $gte: 8 } } },
  { $out: "top_rated_movies" }
])
```

🧠 This will create a new collection `top_rated_movies` that contains all movies with a rating of 8 or higher.

---

✅ **Q2:** Use `$out` to **overwrite** an existing collection `movies_summary` with the aggregated average ratings per movie. This will replace all data in the `movies_summary` collection.

```js
db.movies.aggregate([
  { $group: { _id: "$title", averageRating: { $avg: "$rating" } } },
  { $out: "movies_summary" }
])
```

---

✅ **Q3:** If the collection `movies_summary` already exists, use `$out` to **update** it with a completely new dataset based on the latest aggregation.

```js
db.movies.aggregate([
  { $group: { _id: "$genre", averageRating: { $avg: "$rating" } } },
  { $out: "movies_summary" }
])
```

---

### 3. FAANG-Level Scenarios

- How would you use `$out` in a **batch processing pipeline** to overwrite a collection with fresh aggregated data every night? What considerations should you make regarding concurrency and data integrity during this operation?
- How do you ensure that `$out` doesn't unintentionally **delete important data** in cases where you're working with critical collections? What safeguards or backups should be in place?
- Can you think of a scenario where `$out` could be used for **data synchronization** between different MongoDB instances or environments (e.g., between production and staging)?

---

💡 **Real-World Use Case:**
- Use `$out` to **rebuild daily summary reports** in an e-commerce system where you calculate key metrics like sales, revenue, and product performance, overwriting the report collection with fresh aggregated data each day.
