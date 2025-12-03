#include "db.h"
#include <stdio.h>
#include <string.h>

// callback to display a single contact
int display_contact_callback(void* data, int argc, char** argv, char** azColName)
{
    int* found = (int*)data; // point to a flag
    *found = 1;

    printf("Name : %s\n", argv[0] ? argv[0] : "NULL");
    printf("Phone: %s\n", argv[1] ? argv[1] : "NULL");
    printf("Note : %s\n", argv[2] ? argv[2] : "NULL");
    printf("-----------------------------\n");

    return 0;
}

int delete_contact()
{
    sqlite3* db;
    char* err_msg = 0;
    int rc = connect_db(&db);

    if (rc != SQLITE_OK) {
        return rc;
    }

    int id;
    printf("Enter the ID of the contact to delete: ");
    scanf("%d", &id);
    getchar();

    // show the current info
    char sql_select[128];
    snprintf(sql_select, sizeof(sql_select), "SELECT name, phone, note FROM contacts WHERE id = %d", id);
    printf("\nContact to delete:\n");
    int found = 0;

    rc = sqlite3_exec(db, sql_select, display_contact_callback, &found, &err_msg);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "SQL error: %s\n", err_msg);
        sqlite3_free(err_msg);
        close_db(db);
        return rc;
    }
    if (!found) {
        printf("No contact found with ID %d.\n", id);
        close_db(db);
        return 0;
    }
    // ask for confirmation
    char confirm;
    printf("Are you sure you want to delete this contact? (y/s): ");
    scanf(" %c", &confirm);
    getchar();

    if ('y' != confirm && 'Y' != confirm) {
        printf("Delete cancelled.\n");
        close_db(db);
        return 0;
    }

    // delete the contact
    char sql_delete[128];
    snprintf(sql_delete, sizeof(sql_delete), "DELETE FROM contacts WHERE id = %d;", id);

    rc = sqlite3_exec(db, sql_delete, 0, 0, &err_msg);

    if (rc != SQLITE_OK) {
        fprintf(stderr, "SQL error: %s\n", err_msg);
        sqlite3_free(err_msg);
    } else {
        int changes = sqlite3_changes(db);
        if (0 == changes) {
            printf("No contact deleted (ID %d may not exist).\n", id);
        } else {
            printf("Contact deleted successfully. Back to main menu.\n");
        }
    }
    close_db(db);
    return rc;
}