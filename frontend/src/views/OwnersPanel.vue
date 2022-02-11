<template>
  <v-data-table
    :headers="headers"
    :items="owners"
    sort-by="calories"
    class="elevation-1"
  >
    <template v-slot:top>
      <v-toolbar
        flat
      >
        <v-toolbar-title>Propietarios</v-toolbar-title>
        <v-divider
          class="mx-4"
          inset
          vertical
        ></v-divider>
        <v-spacer></v-spacer>
        <v-dialog
          v-model="dialog"
          max-width="500px"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              color="green"
              dark
              class="mb-2"
              v-bind="attrs"
              v-on="on"
            >
              Nuevo Propietario
            </v-btn>
          </template>
          <v-card>
            <v-card-title>
              <span class="text-h5">{{ formTitle }}</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-alert
                  v-if="errorMessage"
                  border="top"
                  color="red lighten-2"
                  dark
                >
                  {{errorMessage}}
                </v-alert>
                <v-row>
                  <v-col
                    cols="12"
                  >
                    <v-text-field
                      v-model="editedItem.name"
                      small
                      label="Nombre Propietario*"
                      required
                    ></v-text-field>
                  </v-col>
                  <v-col
                    cols="12"
                  >
                    <v-text-field
                      v-model="editedItem.identification"
                      small
                      label="Identificación*"
                      required
                    ></v-text-field>
                  </v-col>
                  <v-col
                    cols="12"
                  >
                    <v-select
                      v-model="editedItem.owner_type"
                      small
                      :items="ownerTypes"
                      label="Tipo propietario*"
                      required
                    ></v-select>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="blue darken-1"
                text
                @click="close"
              >
                Cerrar
              </v-btn>
              <v-btn
                color="blue darken-1"
                text
                @click="saveOwner"
              >
                Guardar
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
        <v-dialog v-model="dialogDelete" max-width="500px">
          <v-card>
            <v-alert
              v-if="errorDeleteMessage"
              border="top"
              color="red lighten-2"
              dark
            >
              {{errorDeleteMessage}}
            </v-alert>
            <v-card-title class="text-h5">¿Esta seguro de eliminar este elemento?</v-card-title>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="closeDelete">Cancelar</v-btn>
              <v-btn color="blue darken-1" text @click="deleteItemConfirm">Confirmar</v-btn>
              <v-spacer></v-spacer>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-toolbar>
    </template>
    <template v-slot:item.actions="{ item }">
      <v-icon
        small
        class="mr-2"
        @click="editItem(item)"
      >
        mdi-pencil
      </v-icon>
      <v-icon
        small
        @click="deleteItem(item)"
      >
        mdi-delete
      </v-icon>
    </template>
  </v-data-table>
</template>

<script>
  import OwnerService from '@/services/OwnerService';

  export default {
    data: () => ({
      errorMessage: '',
      errorDeleteMessage: '',
      ownerTypes: [
        'Persona', 
        'Empresa'
      ],  
      dialog: false,
      dialogDelete: false,
      headers: [
        {
          text: 'Nombre',
          align: 'start',
          sortable: false,
          value: 'name',
        },
        { text: 'Tipo propietario', value: 'owner_type' },
        { text: 'Identificactión', value: 'identification' },
        { text: 'Actions', value: 'actions', sortable: false },
      ],
      owners: [],
      editedIndex: -1,
      editedItem: {
        name: '',
        identification: '',
        owner_type: null,
      },
      defaultItem: {
        name: '',
        identification: '',
        owner_type: null,
      },
    }),

    computed: {
      formTitle () {
        return this.editedIndex === -1 ? 'Crear Propietario' : 'Editar Propietario'
      },
    },

    watch: {
      dialog (val) {
        val || this.close()
      },
      dialogDelete (val) {
        val || this.closeDelete()
      },
    },

    mounted() {
      OwnerService.getOwners()
        .then(resp => {
          console.log(resp)
          this.owners = resp.data;
        })
    },

    methods: {
      editItem (item) {
        this.editedIndex = this.owners.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialog = true
      },

      deleteItem (item) {
        console.log('deleteItem', item.uuid);
        this.editedIndex = this.owners.indexOf(item)
        /* this.editedItem = Object.assign({}, item) */
        this.dialogDelete = true
      },

      deleteItemConfirm () {
        console.log('deleteItem', this.editedIndex);
        OwnerService.deleteOwner(this.owners[this.editedIndex].uuid)
          .then(resp => {
            console.log(resp);
            this.owners.splice(this.editedIndex, 1)
            this.closeDelete()
          })
          .catch(err => {
            console.log(err);
            this.errorDeleteMessage = 'Ocurrio un error al eliminar el propietario'
          })
        
      },

      close () {
        this.dialog = false
        this.$nextTick(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        })
      },

      closeDelete () {
        this.dialogDelete = false
        this.$nextTick(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        })
      },

      cleardata() {
        this.errorMessage = '';
      },

      saveOwner() {
        if (!this.editedItem.name) {
          this.errorMessage = 'Debe ingresar el nombre';
          return
        }
        if (!this.editedItem.identification) {
          this.errorMessage = 'Debe ingresar la identificación';
          return
        }
        if ( !['Persona', 'Empresa'].includes(this.editedItem.owner_type) ) {
          this.errorMessage = 'Debe ingresar el tipo de propietario';
          return
        }

        const realOwnerType = this.editedItem.owner_type === 'Persona' ? 0 : 1;
        if (this.editedIndex > -1) {
          console.log('editar')
          OwnerService.updateOwner(this.editedItem.name, this.editedItem.identification, realOwnerType, this.editedItem.uuid)
            .then(resp => {
              console.log(resp);
              this.cleardata();
              Object.assign(this.owners[this.editedIndex], this.editedItem)
              this.dialog = false;
            })
            .catch(err => {
              console.log(err);
              this.errorMessage = 'Ocurrio un error al registrar el propietario'
            })
        } else {
          OwnerService.createOwner(this.editedItem.name, this.editedItem.identification, realOwnerType)
            .then(resp => {
              console.log(resp);
              this.cleardata();
              this.owners.push(resp.data);
              this.dialog = false;
            })
            .catch(err => {
              console.log(err);
              this.errorMessage = 'Ocurrio un error al registrar el propietario'
            })
        }
        
      }
    },
  }
</script>