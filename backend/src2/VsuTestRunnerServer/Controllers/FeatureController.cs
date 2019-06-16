using System;
using System.Collections.Generic;
using System.Linq;
using Microsoft.AspNetCore.Mvc;
using SharedModels.DTOs;
using SharedModels.Enum;

namespace VsuTestRunnerServer.Controllers
{
    public class FeatureController: BaseApiController
    {
        [HttpGet]
        public List<FeatureModelDto> GetAllowedFeatures()
        {

            var values = Enum.GetValues(typeof(FeatureType)).Cast<FeatureType>();
            var res = values.Select(v => new FeatureModelDto
            {
                Name = v.ToString(),
                Value = v
            }).ToList();
            return res;
        }
    }
}