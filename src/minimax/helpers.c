#include <assert.h>
#include "data_structures.h"

void List_initialize(List* list) {
	list->count = 0;
}

void List_append(List* list, int number) {
	assert(list->count < 32);  // TODO delete this later
			
	list->items[list->count] = number;
	list->count++;
}

int List_item_in_list(List* list, int item) {
	int item_in_list = 0;

	for (int i = 0; i < list->count; i++) {
		if (list->values[i] == item)
			item_in_list = 1;
	}

	return item_in_list;
}

void Dict_initialize(Dict* dict) {
	dict->count = 0;
}

void Dict_put_pair(Dict* dict, int key, int value) {
	assert(dict->count < 32);  // TODO delete this later

	dict->keys[dict->count] = key;
	dict->values[dict->count] = value;
	dict->count++;
}

void Dict_del_pair(Dict* dict, int key) {
	int length_until_deleted_key = 0;

	for (int i = 0; i < dict->count; i++) {
		if (dict->keys[i] == key)
			length_until_deleted_key = i;
	}

	assert(length_until_deleted_key != 0)  // TODO delete this later

	for (int i = length_until_deleted_key; i < dict->count - 1; i++) {
		dict->keys[i] = dict->keys[i + 1];
		dict->values[i] = dict->values[i + 1];
	}

	dict->count--;
}
