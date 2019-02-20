#!/usr/bin/python
# coding=utf-8

__author__ = "Maxime Hutinet, Livio Nagy"
__version__ = "0.0.1"
__status__ = "Finished"


#    LaPieFestivalSearchEngine : Webapp allowing users to find concerts/festivals around them.
#    Copyright (C) 2019  Maxime Hutinet & Livio Nagy

#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

import boto3

def createTable(dynamodb, tableName, primaryKeyName):
    table = dynamodb.create_table(
        TableName=tableName,
        KeySchema=[
            {
                'AttributeName': primaryKeyName,
                'KeyType': 'HASH'
            },

        ],
        AttributeDefinitions=[
            {
                'AttributeName': primaryKeyName,
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    return table


def insertItem(table, data):
    table.put_item(
       Item=data
    )


def getDataFromTable(table, tablePrimaryKeyName, tablePrimaryKeyValue):
    if tablePrimaryKeyValue is not None:
        primaryKeyDict = {tablePrimaryKeyName: tablePrimaryKeyValue}
        response = table.get_item(
            Key=primaryKeyDict
        )
        item = response['Item']
        return item


def addEntryToTable(table, tablePrimaryKeyName, tablePrimaryKeyValue, dataKey, dataValue):
    table.update_item(
        Key={
            tablePrimaryKeyName: tablePrimaryKeyValue
        },
        UpdateExpression='SET ' + dataKey + ' = :val1',
        ExpressionAttributeValues={
            ':val1': dataValue
        }
    )


