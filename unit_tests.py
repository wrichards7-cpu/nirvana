from app.api.member import coalescing, SortType, SortDirection, SortBody, ColumnSortBody, PostAlgoBody, GetCurrentPolicyBody, Columns


#example of unit test testing coalescing function

# def coalescing(input_list, coalesAlgo):

def testCoalescingFunction():

    input_list = [
        [ 10000, 9000, 1000 ],
        [ 20000, 9000, 50000 ],
        [ 10000, 8000, 1000 ]
    ]


    primary_sort_type = SortType.value
    secondary_sort_type = SortType.value
    third_sort_type = SortType.value

    primary_sort_direction = SortDirection.desc
    secondary_sort_direction = SortDirection.asc
    third_sort_direction = SortDirection.desc

    primary_sort_body = SortBody(sort_type = primary_sort_type, sort_direction = primary_sort_direction)
    secondary_sort_body = SortBody(sort_type = secondary_sort_type, sort_direction = secondary_sort_direction)
    third_sort_body = SortBody(sort_type = third_sort_type, sort_direction = third_sort_direction)

    primary_column = ColumnSortBody(column = Columns.oop_max, sort_body=primary_sort_body)
    secondary_column = ColumnSortBody(column = Columns.remaining_oop_max, sort_body=secondary_sort_body)
    third_column = ColumnSortBody(column = Columns.copay, sort_body=third_sort_body)

    postAlgoBody = PostAlgoBody(primary=primary_column, secondary=secondary_column, third=third_column)

    result = coalescing(input_list, postAlgoBody)

    assert result[0] == 20000

testCoalescingFunction()

print('All unit tests passed ....')