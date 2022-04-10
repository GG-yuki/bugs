using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.IO;

namespace FL.Exhibitor.ckeditor
{
    /// <summary>
    /// Upload 的摘要说明
    /// </summary>
    public class Upload : IHttpHandler
    {

        public void ProcessRequest(HttpContext context)
        {
            FL.Entity.t_Company CompanyEnt = FL.BLL.t_Company.GetHttpCompany("");

            if (CompanyEnt.fdID<=0 || CompanyEnt.fdState==0)
            {
                string retMsg = "您的登录已经超时，请重新登录";
                context.Response.Write("<script>alert(\"" + retMsg + "\");</script>");
                context.Response.End();
            }



            HttpPostedFile uploads = context.Request.Files["upload"];
            string CKEditorFuncNum = context.Request["CKEditorFuncNum"];
            string file = System.IO.Path.GetFileName(uploads.FileName);
            string fileExt = System.IO.Path.GetExtension(uploads.FileName).ToLower();
            string fileName = uploads.FileName;
            bool isImg =  fileExt.StartsWith(".jpg") || fileExt.StartsWith(".png") || fileExt.StartsWith(".bmp") || fileExt.StartsWith(".gif");
            if (!isImg)
            {
                string retMsg = "上传失败.文件格式不正确（只允许上传 jpg png bmp gif  格式的图片）";
                context.Response.Write("<script>alert(\"" + retMsg + "\");</script>");
                context.Response.End();
            }


            string directory = "Exhibitor";
            int width = FL.Common.Http.GetIntParam(context.Request, "width", 0);
            int height = FL.Common.Http.GetIntParam(context.Request, "height", 0);
            List<FL.Common.cn.crexpo.img.Img> items = new List<FL.Common.cn.crexpo.img.Img>();
            FL.Common.cn.crexpo.img.Img item = new FL.Common.cn.crexpo.img.Img();
            item.directory = FL.Common.Http.GetStringParam(context.Request, "directory", "");
            item.extendName = Path.GetExtension(uploads.FileName);
            item.width = width;
            item.height = height;
            if (directory.Length > 0)
            {
                item.directory = directory;
            }
            items.Add(item);

            string c = FL.Common.PostImg.Save(uploads, ref items);          

            string url = items[0].url; ;
            context.Response.Write("<script>window.parent.CKEDITOR.tools.callFunction(" + CKEditorFuncNum + ", \"" + url + "\");</script>");
            context.Response.End();
        }

        public bool IsReusable
        {
            get
            {
                return false;
            }
        }
    }
}