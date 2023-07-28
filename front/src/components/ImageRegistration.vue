<template>
    <el-upload
        ref="uploadRef"
        multiple="multiple"
        class="upload-demo"
        drag="drag"
        action="http://127.0.0.1:8010/imgRegistration"
        :auto-upload="false"
        :on-success=handleUploadSuccess
    >
        <template #trigger>
            <el-button type="primary">选择图片</el-button>
        </template>

        <el-button class="ml-3" type="success" @click="submitUpload">
            点击上传
        </el-button>

        <template #tip>
            <div class="el-upload__tip">
                请不要上传除图片外的文件
            </div>
        </template>
    </el-upload>
    <ShowImg v-bind:url=imgurl />
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import type {UploadInstance} from 'element-plus'
import ShowImg from "./ShowImg.vue";

let imgurl = ref("http://127.0.0.1:8010/imgRegistration")
let key = 0
const uploadRef = ref<UploadInstance>()
const submitUpload = () => {
    uploadRef.value!.submit()
}
const handleUploadSuccess = (response: any) => {
    key += 1;
    imgurl.value = "http://127.0.0.1:8010/imgRegistration?key=" + key.toString();
};


</script>
