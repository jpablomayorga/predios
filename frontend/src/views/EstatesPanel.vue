<template>
  <div>
    <v-card
      class="mb-4"
      outlined
    >
      <v-alert
        v-if="alert"
        border="top"
        color="green lighten-2"
        dark
      >
        Se encontraron <b>{{estates.length}}</b> predios en la busqueda
      </v-alert>
      <v-list-item three-line>
        <v-list-item-content>
          <v-list-item-title class="text-h5 mb-1">
            Filtrar predios
          </v-list-item-title>
          <v-row style="zoom:0.8">
            <v-col cols="3">
              <v-text-field
                  v-model="currentFilter.owner_name"
                  small
                  label="Nombre Propietario"
                  required
                ></v-text-field>
            </v-col>
            <v-col cols="3">
              <v-text-field
                  v-model="currentFilter.owner_identification"
                  small
                  label="Identificación Propietario"
                  required
                ></v-text-field>
            </v-col>
            <v-col cols="3">
              <v-text-field
                  v-model="currentFilter.name"
                  small
                  label="Nombre Predio"
                  required
                ></v-text-field>
            </v-col>
            <v-col cols="3">
              <v-text-field
                  v-model="currentFilter.cadastral_certificate"
                  small
                  label="Cedula catastral"
                  required
                ></v-text-field>
            </v-col>
            <v-col cols="3">
              <v-select
                  v-model="currentFilter.estate_type"
                  small
                  :items="estateTypesFilter"
                  label="Tipo predio"
                  required
                ></v-select>
            </v-col>
          </v-row>
        </v-list-item-content>
      </v-list-item>

      <v-card-actions>
        <v-btn
          @click="filterEstates"
          color="blue"
        >
          Filtrar
        </v-btn>
      </v-card-actions>
    </v-card>
    <v-data-table
      :headers="headers"
      :items="estates"
      sort-by="calories"
      class="elevation-1"
    >
      <template v-slot:top>
        <v-toolbar
          flat
        >
          <v-toolbar-title>Predios</v-toolbar-title>
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
                Nuevo predio
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
                        label="Nombre Predio*"
                        required
                      ></v-text-field>
                    </v-col>
                    <v-col
                      cols="12"
                    >
                      <v-text-field
                        v-model="editedItem.cadastral_certificate"
                        small
                        label="Cedula catastral*"
                        required
                      ></v-text-field>
                    </v-col>
                    <v-col
                      cols="12"
                    >
                      <v-text-field
                        v-model="editedItem.estate_registration"
                        small
                        label="Matricula inmobiliaria*"
                        required
                      ></v-text-field>
                    </v-col>
                    <v-col
                      cols="12"
                    >
                      <v-select
                        v-model="editedItem.estate_type"
                        small
                        :items="estateTypes"
                        label="Tipo predio*"
                        required
                      ></v-select>
                    </v-col>
                    <v-col
                      cols="12"
                    >
                      <v-select
                        v-model="selectedOwners"
                        :items="owners"
                        item-text="name"
                        item-value="uuid"
                        chips
                        label="Seleccione propietarios"
                        multiple
                        solo
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
                  @click="saveEstate"
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
      <template v-slot:item.owners_count="{ item }">
        {{item.owners.length}}
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
  </div>
</template>

<script>
  import EstateService from '@/services/EstateService';
  import OwnerService from '@/services/OwnerService';

  export default {
    data: () => ({
      alert: false,
      errorMessage: '',
      errorDeleteMessage: '',
      estateTypes: [
        'Urbano', 
        'Rural'
      ],
      estateTypesFilter: [
        'Urbano', 
        'Rural',
        'Todos'
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
        { text: 'Tipo predio', value: 'estate_type' },
        { text: 'Cedula catastral', value: 'cadastral_certificate' },
        { text: 'Matricula inmobiliria', value: 'estate_registration' },
        { text: 'Número de propietarios', value: 'owners_count' },
        { text: 'Actions', value: 'actions', sortable: false },
      ],
      estates: [],
      owners: [],
      selectedOwners: [],
      editedIndex: -1,
      editedItem: {
        name: '',
        cadastral_certificate: '',
        estate_type: null,
        estate_registration: '',
        owners: []
      },
      defaultItem: {
        name: '',
        cadastral_certificate: '',
        estate_type: null,
        estate_registration: '',
        owners: []
      },
      currentFilter: {
        name: '',
        cadastral_certificate: '',
        owner_name: '',
        owner_identification: '',
        estate_type: 'Todos',
      }
    }),

    computed: {
      formTitle () {
        return this.editedIndex === -1 ? 'Crear Predio' : 'Editar Predio'
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
      EstateService.getEstates()
        .then(resp => {
          this.estates = resp.data;
        })
      OwnerService.getOwners()
        .then(resp => {
          this.owners = resp.data;
        })
    },

    methods: {
      editItem (item) {
        this.editedIndex = this.estates.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.selectedOwners = item.owners.map(x => x.uuid);
        this.dialog = true
      },

      deleteItem (item) {
        console.log('deleteItem', item.uuid);
        this.editedIndex = this.estates.indexOf(item)
        /* this.editedItem = Object.assign({}, item) */
        this.dialogDelete = true
      },

      deleteItemConfirm () {
        console.log('deleteItem', this.editedIndex);
        EstateService.deleteEstate(this.estates[this.editedIndex].uuid)
          .then(resp => {
            console.log(resp);
            this.estates.splice(this.editedIndex, 1)
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

      filterEstates() {
        let filterString = '?';
        if ( this.currentFilter.owner_name !== '' ) {
          filterString += `owner_name=${this.currentFilter.owner_name}&`
        }
        if ( this.currentFilter.owner_identification !== '' ) {
          filterString += `owner_identification=${this.currentFilter.owner_identification}&`
        }
        if ( this.currentFilter.name !== '' ) {
          filterString += `name=${this.currentFilter.name}&`
        }
        if ( this.currentFilter.cadastral_certificate !== '' ) {
          filterString += `cadastral_certificate=${this.currentFilter.cadastral_certificate}&`
        }
        if ( this.currentFilter.estate_type !== 'Todos' ) {
          const estateType = this.currentFilter.estate_type === 'Urbano' ? 0 : 1;
          filterString += `estate_type=${estateType}&`
        }
        EstateService.getEstates(filterString)
          .then(resp => {
            console.log(resp);
            this.estates = resp.data;
            this.alert = true;
            setTimeout(()=>{
              this.alert = false;
            }, 3000)
          })
      },

      saveEstate() {
        if (!this.editedItem.name) {
          this.errorMessage = 'Debe ingresar el nombre';
          return
        }
        if (!this.editedItem.cadastral_certificate) {
          this.errorMessage = 'Debe ingresar la cedula catastral';
          return
        }
        if (!this.editedItem.estate_registration) {
          this.errorMessage = 'Debe ingresar la matricula inmobiliaria';
          return
        }
        if ( !['Rural', 'Urbano'].includes(this.editedItem.estate_type) ) {
          this.errorMessage = 'Debe ingresar el tipo de predio';
          return
        }

        this.editedItem.owners = this.selectedOwners;

        const realEstateType = this.editedItem.estate_type === 'Urbano' ? 0 : 1;
        if (this.editedIndex > -1) {
          console.log('editar')
          EstateService.updateEstate(
            this.editedItem.name,
            this.editedItem.cadastral_certificate,
            this.editedItem.estate_registration,
            realEstateType,
            this.selectedOwners,
            this.editedItem.uuid)
            .then(resp => {
              console.log(resp);
              this.cleardata();
              this.estates.splice(this.editedIndex, 1, this.editedItem)
              this.dialog = false;
            })
            .catch(err => {
              console.log(err);
              this.errorMessage = 'Ocurrio un error al registrar el predio'
            })
        } else {
          EstateService.createEstate(
            this.editedItem.name,
            this.editedItem.cadastral_certificate,
            this.editedItem.estate_registration,
            realEstateType,
            this.selectedOwners)
            .then(resp => {
              console.log(resp);
              this.cleardata();
              this.estates.push(resp.data);
              this.dialog = false;
            })
            .catch(err => {
              console.log(err);
              this.errorMessage = 'Ocurrio un error al registrar el predio'
            })
        }
        
      }
    },
  }
</script>