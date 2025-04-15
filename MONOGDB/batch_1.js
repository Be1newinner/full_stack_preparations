// Source   : Hitesh Chaudhary Youtube Channel
// Title    : Complete MongoDB Aggregation Pipeline Course 
// URL      : https://www.youtube.com/watch?v=vx1C8EyTa7Y

// Q. What is the average age of users

db.users.aggregate([
    {
        group
    }
])

// Q. find the couting of distinct elements with key "fruits" sorted in descending order limited to top 5 results

db.users.aggregate([

    // Stage 1
    {
        $group: {
            _id: "$fruits", // the value will have $ operator attached
            count: {          // count is the custom name it can be anything it will be used in next pipeline
                $sum: 1        // here it means on every counted element add 1 to count variable
            }
        }
    },

    // Stage 2
    {
        $sort: {
            count: -1           // count is the vriable from last stage... 1 means ascending and -1 means descending
        }
    },

    // Stage 3
    {
        $limit: 5
    }
])


