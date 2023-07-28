<script lang="ts" setup>
import { ref } from 'vue'
import type {UploadInstance} from 'element-plus'
import ShowImgList from "./ShowImgList.vue";
import {UploadRawFile} from "element-plus";

let srcList = ref([])
let nameList = []
let jsondata = ref({})
const uploadRef = ref<UploadInstance>()
const submitUpload = () => {
    nameList = []
    uploadRef.value!.submit()
}
const handleUploadSuccess = (response: any) => {
    jsondata = response
    const list = [];
    for (let i = 0; i < nameList.length; i++) {
        const url = `http://127.0.0.1:8010/CrackID?key=${nameList[i]}`;
        list.push(url);
    }
    console.log(list)
    srcList.value = list;
};
const handleBeforeUpload = (rawFile: UploadRawFile)=>{
    nameList.push(rawFile.name)
}
</script>

<template>
    <div class="container">
        <div class="upload-container">
            <el-upload
                ref="uploadRef"
                multiple="multiple"
                class="upload-demo"
                drag="drag"
                action="http://127.0.0.1:8010/CrackID"
                :auto-upload="false"
                :on-success="handleUploadSuccess"
                :before-upload="handleBeforeUpload"
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
            <ShowImgList :srcList="srcList" />
        </div>

        <div class="result-container">
            <h2>裂缝识别结果</h2>
            <div v-for="(cracks, imageName) in jsondata" :key="imageName">
                <h3>{{ imageName }}</h3>
                <div v-for="(crack, index) in cracks" :key="index">
                    <p>{{ `裂缝序号: ${index}` }}</p>
                    <p>{{ `长度: ${crack.length}mm` }}</p>
                    <p>{{ `角度: ${crack.angle}` }}</p>
                </div>
            </div>
        </div>
    </div>
</template>

<style>
.container {
    display: flex;
}

.upload-container {
    flex: 1;
}

.result-container {
    flex: 1;
    margin-left: 20px;
}
</style>


