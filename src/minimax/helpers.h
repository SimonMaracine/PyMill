#define MIN(a, b) (((a) < (b)) ? (a) : (b))
#define MAX(a, b) (((a) > (b)) ? (a) : (b))


typedef struct {
	int a, b;
} Tuple;


typedef struct {
	int keys[32];
	int values[32];
	int count;
} Dict;


typedef struct {
	int items[32];
	int count;
} List;


void List_initialize(List* list);
void List_append(List* list, int number);
int List_item_in_list(List* list, int item);

void Dict_initialize(Dict* dict);
void Dict_put_pair(Dict* dict, int key, int value);
void Dict_del_pair(Dict* dict, int key);
